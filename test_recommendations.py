"""
Test dosyası - Ürün tavsiye sistemi için test senaryoları
"""

from main import load_and_prepare_data, create_rules, get_recommendations, print_recommendations
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_recommendation_system():
    """Ana test fonksiyonu"""
    try:
        print("="*60)
        print("🧪 ÜRÜN TAVSİYE SİSTEMİ TEST")
        print("="*60)
        
        # Veriyi yükle
        print("\n1️⃣ Veri yükleniyor...")
        basket_matrix = load_and_prepare_data('Market_Basket_Optimisation.csv')
        print(f"✅ Veri yüklendi: {basket_matrix.shape}")
        
        # Kuralları oluştur
        print("\n2️⃣ Birliktelik kuralları oluşturuluyor...")
        rules = create_rules(basket_matrix, min_support=0.01, min_confidence=0.1)
        print(f"✅ {len(rules)} kural oluşturuldu")
        
        # Test sepetleri
        test_baskets = [
            ['ground beef', 'eggs'],
            ['milk', 'chocolate'],
            ['spaghetti', 'olive oil'],
            ['mineral water', 'chicken'],
            ['frozen vegetables', 'pasta']
        ]
        
        # Her sepet için test
        print("\n3️⃣ Test sepetleri için tavsiyeler üretiliyor...")
        print("="*60)
        
        for i, basket in enumerate(test_baskets, 1):
            print(f"\n📦 TEST {i}/{len(test_baskets)}")
            recommendations = get_recommendations(basket, rules, max_recommendations=5)
            print_recommendations(basket, recommendations)
        
        print("\n" + "="*60)
        print("✅ Tüm testler tamamlandı!")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"\n❌ Dosya hatası: {str(e)}")
        print("💡 Market_Basket_Optimisation.csv dosyasının proje klasöründe olduğundan emin olun.")
    except Exception as e:
        print(f"\n❌ Test hatası: {str(e)}")
        logger.exception("Detaylı hata bilgisi:")


if __name__ == "__main__":
    test_recommendation_system()


