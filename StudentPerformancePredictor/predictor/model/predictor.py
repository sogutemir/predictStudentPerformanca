import os
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from django.conf import settings

def load_model(model_path=None):
    """
    Kaydedilmiş bir modeli yükler.
    """
    try:
        if model_path is None:
            model_path = os.path.join(settings.BASE_DIR, 'predictor', 'model', 'linear_regression_model.pkl')
            
        if not os.path.exists(model_path):
            # Model yoksa örnek model oluştur
            print(f"Model dosyası {model_path} bulunamadı. Örnek model oluşturuluyor...")
            result = create_sample_model(model_path)
            if not result.get("success"):
                return None
        
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        print(f"Model dosyası {model_path} bulunamadı.")
        return None
    except Exception as e:
        print(f"Model yüklenirken hata oluştu: {e}")
        return None

def predict_performance(input_data):
    """
    Verilen girdilere göre öğrenci performansını tahmin eder.
    """
    try:
        model = load_model()
        
        if model is None:
            return {"error": "Model yüklenemedi. Lütfen önce model oluşturun.", "success": False}
        
        if float(input_data.get('daily_social_media', 0)) > 90:
            excess_social_media_minutes = float(input_data.get('daily_social_media', 0)) - 90
            social_media_penalty = excess_social_media_minutes * -0.15
        else:
            social_media_penalty = 0
        
        features = prepare_features(input_data)
        
        print("Öznitelik vektörü:", features)
        
        print("Model katsayıları:", model.coef_)
        
        print("Sosyal medya cezası:", social_media_penalty)
        
        prediction = model.predict([features])[0]
        
        final_prediction = prediction + social_media_penalty
        
        return {
            "input_data": input_data,
            "predicted_score": round(float(final_prediction), 2),
            "success": True
        }
    
    except Exception as e:
        return {"error": str(e), "success": False}

def prepare_features(input_data):
    """
    Tahmin için öznitelikleri hazırlar.
    """
    for key in input_data:
        if input_data[key] == '':
            input_data[key] = 0
    
    numeric_features = [
        float(input_data.get('gpa', 0)),
        float(input_data.get('avg_exam_score', 0)),
        float(input_data.get('absent_rate', 0)),
        float(input_data.get('daily_study', 0)),
        float(input_data.get('anxiety_score', 0)),
        float(input_data.get('motivation_score', 0)),
        float(input_data.get('avg_sleep_time', 0)),
        float(input_data.get('daily_social_media', 0))
    ]
    
    categorical_features = []
    
    for feature in ['cram_school', 'private_lesson', 'private_room', 'study_resources']:
        if input_data.get(feature) == 'yes':
            categorical_features.append(1)
        else:
            categorical_features.append(0)
    
    parent_edu = input_data.get('parent_edu', 'p')
    parent_edu_features = [0, 0, 0, 0]  # p, m, h, u
    
    if parent_edu == 'p':
        parent_edu_features[0] = 1
    elif parent_edu == 'm':
        parent_edu_features[1] = 1
    elif parent_edu == 'h':
        parent_edu_features[2] = 1
    elif parent_edu == 'u':
        parent_edu_features[3] = 1
    
    categorical_features.extend(parent_edu_features)
    
    features = numeric_features + categorical_features
    
    return features

def create_dummy_model(model_path=None):
    """
    Basit bir dummy model oluşturur ve kaydeder.
    """
    try:
        model = LinearRegression()
        
        X = np.random.rand(100, 16)
        y = np.random.rand(100) * 500
        
        model.fit(X, y)
        
        if model_path is None:
            model_path = os.path.join(settings.BASE_DIR, 'predictor', 'model', 'linear_regression_model.pkl')
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)
        
        return {"success": True, "message": "Dummy model başarıyla oluşturuldu ve kaydedildi."}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_sample_model(model_path=None):
    """
    Örnek bir model oluşturur ve kaydeder.
    """
    try:
        np.random.seed(42)
        n_samples = 200
        
        gpa = np.random.normal(75, 10, n_samples)
        avg_exam_score = np.random.normal(350, 50, n_samples)
        absent_rate = np.random.beta(2, 10, n_samples)
        daily_study = np.random.gamma(5, 30, n_samples)
        anxiety_score = np.random.randint(1, 11, n_samples)
        motivation_score = np.random.randint(1, 11, n_samples)
        avg_sleep_time = np.random.normal(420, 60, n_samples)
        daily_social_media = np.random.gamma(3, 20, n_samples)
        
        cram_school = np.random.choice([0, 1], n_samples)
        private_lesson = np.random.choice([0, 1], n_samples)
        private_room = np.random.choice([0, 1], n_samples)
        study_resources = np.random.choice([0, 1], n_samples)
        
        parent_edu_p = np.zeros(n_samples)
        parent_edu_m = np.zeros(n_samples)
        parent_edu_h = np.zeros(n_samples)
        parent_edu_u = np.zeros(n_samples)
        
        for i in range(n_samples):
            edu = np.random.choice(['p', 'm', 'h', 'u'])
            if edu == 'p':
                parent_edu_p[i] = 1
            elif edu == 'm':
                parent_edu_m[i] = 1
            elif edu == 'h':
                parent_edu_h[i] = 1
            else:
                parent_edu_u[i] = 1
        
        X = np.column_stack([
            gpa, avg_exam_score, absent_rate, daily_study, anxiety_score, 
            motivation_score, avg_sleep_time, daily_social_media,
            cram_school, private_lesson, private_room, study_resources,
            parent_edu_p, parent_edu_m, parent_edu_h, parent_edu_u
        ])
        
        y = (
            -0.0219 * gpa + 
            0.8377 * avg_exam_score + 
            -8.6282 * absent_rate + 
            0.1500 * daily_study + 
            -1.6082 * anxiety_score + 
            3.4378 * motivation_score +
            0.0396 * avg_sleep_time +
            -0.0500 * daily_social_media +
            7.8000 * cram_school +
            6.5731 * private_lesson +
            -2.1106 * private_room +
            1.6720 * study_resources +
            -2.4629 * parent_edu_p +
            -1.0072 * parent_edu_m +
            1.5278 * parent_edu_h +
            1.9423 * parent_edu_u +
            np.random.normal(0, 20, n_samples)
        )
        
        model = LinearRegression()
        model.fit(X, y)
        
        if model_path is None:
            model_path = os.path.join(settings.BASE_DIR, 'predictor', 'model', 'linear_regression_model.pkl')
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)
        
        return {"success": True, "message": "Örnek model başarıyla oluşturuldu ve kaydedildi."}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
