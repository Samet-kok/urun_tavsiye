# Ürün Tavsiye Sistemi

Market Basket Analysis (Sepet Analizi) kullanarak ürün tavsiye sistemi. Apriori algoritması ile birliktelik kuralları oluşturulur ve sepetteki ürünlere göre tavsiyeler üretilir.

## ✨ Özellikler

- 🛒 Market basket verilerinden sık öğe kümelerini bulma
- 🔍 Apriori algoritması ile birliktelik kuralları oluşturma
- 💡 Sepetteki ürünlere göre akıllı ürün tavsiyeleri
- 📊 Confidence, Lift ve Support metrikleri ile tavsiye skorlama
- ⚡ Performans optimizasyonu (vektörel işlemler)
- 🛡️ Hata yönetimi ve veri doğrulama
- 📝 Detaylı logging sistemi
- ⚙️ Konfigürasyon dosyası ile kolay ayarlama

## 📋 Gereksinimler

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- mlxtend >= 0.19.0

## 🚀 Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/Samet-kok/urun_tavsiye.git
cd urun_tavsiye
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## 💻 Kullanım

### Temel Kullanım

1. `Market_Basket_Optimisation.csv` dosyasını [Kaggle'dan indirin](https://www.kaggle.com/datasets/hemanthkumar05/market-basket-optimization) ve proje klasörüne yerleştirin.

2. Ana programı çalıştırın:
```bash
python main.py
```

### Test Senaryoları

Test dosyasını çalıştırın:
```bash
python test_recommendations.py
```

### Örnek Kullanımlar

Farklı kullanım senaryolarını görmek için:
```bash
python example_usage.py
```

## 📚 API Dokümantasyonu

### `load_and_prepare_data(file_path: str) -> pd.DataFrame`
CSV dosyasından veriyi yükler ve one-hot encoding matrisine dönüştürür.

**Parametreler:**
- `file_path`: CSV dosyasının yolu

**Döndürür:**
- One-hot encoding ile hazırlanmış basket matrix

**Hatalar:**
- `FileNotFoundError`: Dosya bulunamazsa
- `ValueError`: Veri formatı geçersizse

### `create_rules(basket_matrix, min_support=0.01, min_confidence=0.1) -> pd.DataFrame`
Apriori algoritması ile birliktelik kuralları oluşturur.

**Parametreler:**
- `basket_matrix`: One-hot encoding matrisi
- `min_support`: Minimum destek değeri (0-1 arası, varsayılan: 0.01)
- `min_confidence`: Minimum güven değeri (0-1 arası, varsayılan: 0.1)

**Döndürür:**
- Birliktelik kuralları DataFrame'i

### `get_recommendations(basket_items, rules, min_confidence=0.1, min_lift=1.5, max_recommendations=10) -> Dict`
Sepetteki ürünlere göre tavsiye edilen ürünleri döndürür.

**Parametreler:**
- `basket_items`: Sepetteki ürünlerin listesi
- `rules`: Birliktelik kuralları DataFrame'i
- `min_confidence`: Minimum güven filtresi (varsayılan: 0.1)
- `min_lift`: Minimum lift filtresi (varsayılan: 1.5)
- `max_recommendations`: Maksimum tavsiye sayısı (varsayılan: 10)

**Döndürür:**
- Tavsiye edilen ürünler ve metrikleri içeren dictionary

## 📖 Örnek Kullanım

```python
from main import load_and_prepare_data, create_rules, get_recommendations
import config

# Veriyi yükle
basket_matrix = load_and_prepare_data(config.DATA_FILE)

# Kuralları oluştur
rules = create_rules(
    basket_matrix,
    min_support=config.MIN_SUPPORT,
    min_confidence=config.MIN_CONFIDENCE
)

# Sepet için tavsiye al
basket = ['ground beef', 'eggs']
recommendations = get_recommendations(
    basket,
    rules,
    min_lift=config.MIN_LIFT,
    max_recommendations=config.MAX_RECOMMENDATIONS
)

# Sonuçları göster
for product, metrics in recommendations.items():
    print(f"{product}: Skor={metrics['score']:.2%}, "
          f"Güven={metrics['confidence']:.2%}, "
          f"Lift={metrics['lift']:.2f}")
```

## ⚙️ Konfigürasyon

`config.py` dosyasından parametreleri özelleştirebilirsiniz:

- `MIN_SUPPORT`: Minimum destek değeri
- `MIN_CONFIDENCE`: Minimum güven değeri
- `MIN_LIFT`: Minimum lift değeri
- `MAX_RECOMMENDATIONS`: Maksimum tavsiye sayısı
- `CONFIDENCE_WEIGHT`: Skorlama için confidence ağırlığı
- `LIFT_WEIGHT`: Skorlama için lift ağırlığı

## 🏗️ Proje Yapısı

```
urun_tavsiye/
├── main.py                    # Ana modül (fonksiyonlar)
├── config.py                  # Konfigürasyon dosyası
├── test_recommendations.py    # Test senaryoları
├── example_usage.py           # Örnek kullanımlar
├── requirements.txt           # Python bağımlılıkları
├── README.md                  # Bu dosya
├── LICENSE                    # MIT Lisansı
└── Market_Basket_Optimisation.csv  # Veri dosyası (Kaggle'dan indirilmeli)
```

## 🔧 İyileştirmeler

Bu versiyonda yapılan iyileştirmeler:

- ✅ Hata yönetimi ve veri doğrulama eklendi
- ✅ Performans optimizasyonu (iterrows yerine vektörel işlemler)
- ✅ Type hints eklendi
- ✅ Detaylı logging sistemi
- ✅ Konfigürasyon dosyası
- ✅ Test ve örnek kullanım dosyaları
- ✅ Geliştirilmiş dokümantasyon
- ✅ Daha iyi hata mesajları

## 📝 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

