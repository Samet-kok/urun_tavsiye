"""
Ürün Tavsiye Sistemi - Market Basket Analysis
Apriori algoritması kullanarak birliktelik kuralları oluşturur ve ürün tavsiyeleri üretir.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    """
    CSV dosyasından veriyi yükler ve one-hot encoding matrisine dönüştürür.
    
    Args:
        file_path: CSV dosyasının yolu
        
    Returns:
        One-hot encoding ile hazırlanmış basket matrix
        
    Raises:
        FileNotFoundError: Dosya bulunamazsa
        ValueError: Veri formatı geçersizse
    """
    try:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
        
        logger.info(f"Veri yükleniyor: {file_path}")
        df = pd.read_csv(file_path, header=None)
        
        if df.empty:
            raise ValueError("CSV dosyası boş!")
        
        logger.info(f"Yüklenen satır sayısı: {len(df)}")
        
        # Boş değerleri temizle
        df = df.fillna('')
        
        # Tüm ürünlerin listesini oluştur (daha verimli yöntem)
        all_products = set()
        for col in df.columns:
            unique_products = df[col].unique()
            all_products.update(unique_products)
        all_products.discard('')
        
        if not all_products:
            raise ValueError("Veri setinde geçerli ürün bulunamadı!")
        
        logger.info(f"Toplam benzersiz ürün sayısı: {len(all_products)}")
        
        # One-hot encoding matrisini oluştur (performans optimizasyonu)
        basket_matrix = pd.DataFrame(0, index=df.index, columns=sorted(all_products), dtype=int)
        
        # Vektörel işlemlerle doldur (iterrows yerine daha verimli)
        for idx, row in df.iterrows():
            # Her satırdaki ürünleri al
            products_in_row = [product for product in row if product != '']
            if products_in_row:
                basket_matrix.loc[idx, products_in_row] = 1
        
        logger.info(f"Basket matrix oluşturuldu: {basket_matrix.shape}")
        return basket_matrix
        
    except FileNotFoundError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Veri yükleme hatası: {str(e)}")
        raise ValueError(f"Veri yükleme başarısız: {str(e)}")


def create_rules(
    basket_matrix: pd.DataFrame,
    min_support: float = 0.01,
    min_confidence: float = 0.1
) -> pd.DataFrame:
    """
    Apriori algoritması ile birliktelik kuralları oluşturur.
    
    Args:
        basket_matrix: One-hot encoding ile hazırlanmış basket matrix
        min_support: Minimum destek değeri (0-1 arası)
        min_confidence: Minimum güven değeri (0-1 arası)
        
    Returns:
        Birliktelik kuralları DataFrame'i
        
    Raises:
        ValueError: Parametreler geçersizse veya kurallar oluşturulamazsa
    """
    try:
        if not (0 < min_support <= 1):
            raise ValueError("min_support 0 ile 1 arasında olmalıdır")
        if not (0 < min_confidence <= 1):
            raise ValueError("min_confidence 0 ile 1 arasında olmalıdır")
        
        logger.info(f"Birliktelik kuralları oluşturuluyor (min_support={min_support}, min_confidence={min_confidence})")
        
        # Sık öğe kümelerini bul
        frequent_itemsets = apriori(
            basket_matrix,
            min_support=min_support,
            use_colnames=True,
            verbose=0
        )
        
        if frequent_itemsets.empty:
            logger.warning("Sık öğe kümesi bulunamadı. min_support değerini düşürmeyi deneyin.")
            return pd.DataFrame()
        
        logger.info(f"Bulunan sık öğe kümesi sayısı: {len(frequent_itemsets)}")
        
        # Birliktelik kurallarını oluştur
        rules = association_rules(
            frequent_itemsets,
            metric="confidence",
            min_threshold=min_confidence
        )
        
        if rules.empty:
            logger.warning("Birliktelik kuralı oluşturulamadı. min_confidence değerini düşürmeyi deneyin.")
            return pd.DataFrame()
        
        # Kuralları confidence ve lift değerlerine göre sırala
        rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
        
        logger.info(f"Oluşturulan kural sayısı: {len(rules)}")
        return rules
        
    except Exception as e:
        logger.error(f"Kural oluşturma hatası: {str(e)}")
        raise


def get_recommendations(
    basket_items: List[str],
    rules: pd.DataFrame,
    min_confidence: float = 0.1,
    min_lift: float = 1.5,
    max_recommendations: int = 10
) -> Dict[str, Dict[str, float]]:
    """
    Sepetteki ürünlere göre tavsiyeler üretir.

    Args:
        basket_items: Sepetteki ürünlerin listesi
        rules: Birliktelik kuralları DataFrame'i
        min_confidence: Minimum güven değeri filtresi
        min_lift: Minimum lift değeri filtresi
        max_recommendations: Maksimum tavsiye sayısı

    Returns:
        Tavsiye edilen ürünler ve metrikleri içeren dictionary
    """
    if not basket_items:
        logger.warning("Sepet boş!")
        return {}
    
    if rules.empty:
        logger.warning("Kural bulunamadı!")
        return {}
    
    recommendations = {}
    basket_set = frozenset(basket_items)
    
    logger.info(f"Sepet için tavsiye aranıyor: {basket_items}")
    
    # Kuralları filtrele (performans için)
    filtered_rules = rules[
        (rules['confidence'] >= min_confidence) & 
        (rules['lift'] >= min_lift)
    ]
    
    if filtered_rules.empty:
        logger.warning("Filtrelenmiş kural bulunamadı!")
        return {}
    
    # Tüm kuralları kontrol et
    for idx, row in filtered_rules.iterrows():
        antecedents = set(row["antecedents"])
        
        # Eğer kural sepetteki ürünlerle eşleşiyorsa
        if antecedents.issubset(basket_set):
            # Tavsiye edilecek ürünleri al (birden fazla olabilir)
            consequents = list(row["consequents"])
            
            for consequent in consequents:
                # Eğer tavsiye edilecek ürün zaten sepette yoksa
                if consequent not in basket_set:
                    # Skor hesapla (confidence ve lift ağırlıklı)
                    score = (row["confidence"] * 0.7) + (row["lift"] * 0.3)
                    
                    # Eğer ürün zaten önerilmişse, daha yüksek skoru kullan
                    if consequent not in recommendations or score > recommendations[consequent]["score"]:
                        recommendations[consequent] = {
                            "score": score,
                            "confidence": row["confidence"],
                            "lift": row["lift"],
                            "support": row["support"]
                        }
    
    # Tavsiyeleri skora göre sırala ve limit uygula
    sorted_recommendations = dict(
        sorted(recommendations.items(), key=lambda x: x[1]["score"], reverse=True)[:max_recommendations]
    )
    
    logger.info(f"Bulunan tavsiye sayısı: {len(sorted_recommendations)}")
    return sorted_recommendations


def print_recommendations(basket_items: List[str], recommendations: Dict[str, Dict[str, float]]) -> None:
    """
    Tavsiyeleri güzel bir formatta yazdırır.
    
    Args:
        basket_items: Sepetteki ürünler
        recommendations: Tavsiye dictionary'si
    """
    print("\n" + "="*60)
    print(f"Sepetteki ürünler: {', '.join(basket_items)}")
    print("="*60)
    
    if recommendations:
        print(f"\n📦 Tavsiye edilen ürünler ({len(recommendations)} adet):\n")
        for i, (product, metrics) in enumerate(recommendations.items(), 1):
            print(f"{i}. {product}:")
            print(f"   ⭐ Skor: {metrics['score']:.2%}")
            print(f"   📊 Güven: {metrics['confidence']:.2%}")
            print(f"   📈 Lift: {metrics['lift']:.2f}")
            print(f"   📉 Destek: {metrics['support']:.2%}")
            print()
    else:
        print("\n❌ Bu sepet için tavsiye bulunamadı.")
        print("💡 İpucu: min_confidence veya min_lift değerlerini düşürmeyi deneyin.")


if __name__ == "__main__":
    # Test için örnek kullanım
    try:
        # Veriyi yükle ve hazırla
        basket_matrix = load_and_prepare_data('Market_Basket_Optimisation.csv')
        
        # Birliktelik kurallarını oluştur
        rules = create_rules(basket_matrix, min_support=0.01, min_confidence=0.1)
        
        # Test sepetleri
        test_baskets = [
            ['ground beef', 'eggs'],
            ['milk', 'chocolate'],
            ['spaghetti', 'olive oil']
        ]
        
        # Her sepet için tavsiye al
        for basket in test_baskets:
            recommendations = get_recommendations(basket, rules, max_recommendations=5)
            print_recommendations(basket, recommendations)
            
    except Exception as e:
        logger.error(f"Program hatası: {str(e)}", exc_info=True)
        print(f"\n❌ Hata oluştu: {str(e)}")
