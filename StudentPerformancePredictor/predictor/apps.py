from django.apps import AppConfig
import os
from django.conf import settings


class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'

    def ready(self):
        # İçe aktarma döngüsünü önlemek için içeride import ediyoruz
        from .model.predictor import load_model
        
        # Uygulama başladığında modelin varlığını kontrol et
        # Model yoksa ve debug modunda isek konsolda mesaj göster
        model_path = os.path.join(settings.BASE_DIR, 'predictor', 'model', 'linear_regression_model.pkl')
        if not os.path.exists(model_path) and settings.DEBUG:
            print("\n[!] Uyarı: Model dosyası bulunamadı.")
            print(f"[!] Beklenen konum: {model_path}")
            print("[!] Modeli oluşturmak için /model/create/ veya /model/create-sample/ URL'lerini kullanabilirsiniz.")
            print("[!] Örneğin: http://localhost:8000/model/create-sample/\n")
