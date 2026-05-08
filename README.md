# Ürün Tavsiye Sistemi (Market Basket Analysis)

Bu projede, müşterilerin sepet verilerini (Market Basket Analysis) inceleyerek ürün tavsiyeleri üreten bir sistem geliştirdim. Temelinde Apriori algoritmasını kullanarak ürünler arasındaki birliktelik kurallarını çıkarıyorum.

## Ne İşe Yarıyor?
- Veri seti üzerinden sık birlikte alınan ürünleri tespit ediyor.
- Apriori algoritması ile birliktelik (association) kuralları oluşturuyor.
- Sepetteki mevcut ürünlere bakarak; Confidence, Lift ve Support metriklerine göre yeni ürünler tavsiye ediyor.

## Kullanılan Teknolojiler
- Python
- Pandas, NumPy
- mlxtend (Apriori ve kurallar için)

## Kurulum ve Çalıştırma

1. Projeyi bilgisayarınıza indirin:
   ```bash
   git clone https://github.com/Samet-kok/urun_tavsiye.git
   cd urun_tavsiye
   ```

2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

3. Kaggle üzerinden [Market Basket Optimisation](https://www.kaggle.com/datasets/hemanthkumar05/market-basket-optimization) veri setini indirip `Market_Basket_Optimisation.csv` adıyla proje dizinine ekleyin.

4. Ana kodu çalıştırın:
   ```bash
   python main.py
   # veya farklı senaryoları test etmek için
   python test_recommendations.py
   ```

## Proje Yapısı ve Önemli Fonksiyonlar
Projeyi olabildiğince modüler ve temiz tutmaya çalıştım:
- `main.py`: Ana işlemlerin yapıldığı dosya.
  - `load_and_prepare_data()`: Veriyi okuyup algoritmanın anlayacağı matris formatına çevirir.
  - `create_rules()`: Apriori ile kural setini oluşturur.
  - `get_recommendations()`: Parametre olarak verdiğiniz sepete en uygun ürünleri listeler.
- `config.py`: Minimum support, confidence ve lift gibi ayarları buradan hızlıca değiştirebilirsiniz.

### Kod İçinden Örnek Kullanım
```python
from main import load_and_prepare_data, create_rules, get_recommendations
import config

# Veriyi hazırlayıp kuralları çıkarıyoruz
basket_matrix = load_and_prepare_data(config.DATA_FILE)
rules = create_rules(basket_matrix, min_support=config.MIN_SUPPORT, min_confidence=config.MIN_CONFIDENCE)

# Sepetinde kıyma ve yumurta olan birine ne önerebiliriz?
basket = ['ground beef', 'eggs']
recommendations = get_recommendations(basket, rules, min_lift=config.MIN_LIFT)

for product, metrics in recommendations.items():
    print(f"{product} -> Güven: {metrics['confidence']:.2%}, Lift: {metrics['lift']:.2f}")
```

## Yaptığım Bazı İyileştirmeler
Kodun daha stabil ve hızlı çalışması için sonradan şu eklemeleri yaptım:
- Pandas üzerinde döngüler (`iterrows`) yerine vektörel işlemler kullanarak performansı epey artırdım.
- Olası veri formatı hatalarını rahat çözebilmek için logging ve temel hata yönetimi (try-except) ekledim.
- Fonksiyonların ne döndürdüğünün anlaşılması için type hint'ler ekledim.
