#!/usr/bin/env python
import os
import django

# Django ortamını ayarla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentPerformancePredictor.settings')
django.setup()

# Model oluşturma fonksiyonunu içe aktar
from predictor.model.predictor import create_sample_model

# Modeli oluştur
result = create_sample_model()
print("Model oluşturma sonucu:", result) 