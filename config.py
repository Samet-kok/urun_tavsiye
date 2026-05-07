"""
Konfigürasyon dosyası - Proje ayarları
"""

# Veri dosyası ayarları
DATA_FILE = 'Market_Basket_Optimisation.csv'

# Apriori algoritması parametreleri
MIN_SUPPORT = 0.01  # Minimum destek değeri (0-1 arası)
MIN_CONFIDENCE = 0.1  # Minimum güven değeri (0-1 arası)

# Tavsiye sistemi parametreleri
MIN_LIFT = 1.5  # Minimum lift değeri
MAX_RECOMMENDATIONS = 10  # Maksimum tavsiye sayısı

# Skorlama ağırlıkları
CONFIDENCE_WEIGHT = 0.7  # Confidence ağırlığı
LIFT_WEIGHT = 0.3  # Lift ağırlığı

# Logging ayarları
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


