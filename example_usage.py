"""
Örnek kullanım - Ürün tavsiye sistemi nasıl kullanılır?
"""

from main import load_and_prepare_data, create_rules, get_recommendations, print_recommendations
import config


def example_basic_usage():
    """Temel kullanım örneği"""
    print("="*60)
    print("📚 ÖRNEK KULLANIM - Temel")
    print("="*60)
    
    # 1. Veriyi yükle
    basket_matrix = load_and_prepare_data(config.DATA_FILE)
    
    # 2. Kuralları oluştur
    rules = create_rules(
        basket_matrix,
        min_support=config.MIN_SUPPORT,
        min_confidence=config.MIN_CONFIDENCE
    )
    
    # 3. Sepet için tavsiye al
    my_basket = ['ground beef', 'eggs']
    recommendations = get_recommendations(
        my_basket,
        rules,
        min_lift=config.MIN_LIFT,
        max_recommendations=config.MAX_RECOMMENDATIONS
    )
    
    # 4. Sonuçları göster
    print_recommendations(my_basket, recommendations)


def example_custom_parameters():
    """Özel parametrelerle kullanım örneği"""
    print("\n" + "="*60)
    print("📚 ÖRNEK KULLANIM - Özel Parametreler")
    print("="*60)
    
    basket_matrix = load_and_prepare_data(config.DATA_FILE)
    
    # Daha sıkı kurallar için parametreleri ayarla
    rules = create_rules(
        basket_matrix,
        min_support=0.02,  # Daha yüksek destek
        min_confidence=0.3  # Daha yüksek güven
    )
    
    my_basket = ['milk', 'chocolate']
    recommendations = get_recommendations(
        my_basket,
        rules,
        min_confidence=0.3,  # Daha yüksek güven filtresi
        min_lift=2.0,  # Daha yüksek lift filtresi
        max_recommendations=5  # Sadece en iyi 5 tavsiye
    )
    
    print_recommendations(my_basket, recommendations)


def example_multiple_baskets():
    """Birden fazla sepet için toplu işlem örneği"""
    print("\n" + "="*60)
    print("📚 ÖRNEK KULLANIM - Toplu İşlem")
    print("="*60)
    
    basket_matrix = load_and_prepare_data(config.DATA_FILE)
    rules = create_rules(basket_matrix)
    
    # Birden fazla sepet
    baskets = [
        ['spaghetti', 'olive oil'],
        ['mineral water', 'chicken'],
        ['frozen vegetables', 'pasta']
    ]
    
    print(f"\n📦 {len(baskets)} sepet için tavsiyeler üretiliyor...\n")
    
    for basket in baskets:
        recommendations = get_recommendations(basket, rules)
        print_recommendations(basket, recommendations)


if __name__ == "__main__":
    try:
        example_basic_usage()
        example_custom_parameters()
        example_multiple_baskets()
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")


