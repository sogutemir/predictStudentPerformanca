from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import PredictionForm
from .models import PredictionHistory
import json
import os

# Model fonksiyonlarını doğru şekilde import et
try:
    from .model.predictor import predict_performance, create_dummy_model, create_sample_model
except ImportError as e:
    print(f"Model import hatası: {e}")
    # Fallback fonksiyonlar
    def predict_performance(input_data):
        return {"error": "Model yüklenemedi", "success": False}
    
    def create_dummy_model():
        return {"error": "Model oluşturulamadı", "success": False}
    
    def create_sample_model():
        return {"error": "Model oluşturulamadı", "success": False}

def home(request):
    """Ana sayfa view'i"""
    context = {
        'request': request,  # Context'e request ekle
    }
    return render(request, 'predictor/home.html', context)

def prediction_form(request):
    """Tahmin formu view'i"""
    context = {
        'request': request,  # Context'e request ekle
    }
    
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Form verilerini al
            input_data = {
                'gpa': form.cleaned_data['gpa'],
                'avg_exam_score': form.cleaned_data['avg_exam_score'],
                'absent_rate': form.cleaned_data['absent_rate'],
                'daily_study': form.cleaned_data['daily_study'],
                'avg_sleep_time': form.cleaned_data['avg_sleep_time'],
                'daily_social_media': form.cleaned_data['daily_social_media'],
                'anxiety_score': form.cleaned_data['anxiety_score'],
                'motivation_score': form.cleaned_data['motivation_score'],
                'parent_edu': form.cleaned_data['parent_edu'],
                'cram_school': form.cleaned_data['cram_school'],
                'private_lesson': form.cleaned_data['private_lesson'],
                'private_room': form.cleaned_data['private_room'],
                'study_resources': form.cleaned_data['study_resources']
            }
            
            # Debug için form verilerini yazdır
            print("Formdan gelen veriler:", input_data)
            
            # Tahmin yap
            prediction_result = predict_performance(input_data)
            
            # Debug için tahmin sonucunu yazdır
            print("Tahmin sonucu:", prediction_result)
            
            if prediction_result.get('success', False):
                # Tahmin sonucunu veritabanına kaydet
                try:
                    PredictionHistory.objects.create(
                        gpa=input_data.get('gpa', 0),
                        avg_exam_score=input_data.get('avg_exam_score', 0),
                        absent_rate=input_data.get('absent_rate', 0),
                        daily_study=input_data.get('daily_study', 0),
                        cram_school=input_data.get('cram_school', 'no'),
                        private_lesson=input_data.get('private_lesson', 'no'),
                        private_room=input_data.get('private_room', 'no'),
                        parent_edu=input_data.get('parent_edu', 'p'),
                        study_resources=input_data.get('study_resources', 'no'),
                        anxiety_score=input_data.get('anxiety_score', 0),
                        motivation_score=input_data.get('motivation_score', 0),
                        avg_sleep_time=input_data.get('avg_sleep_time', 0),
                        daily_social_media=input_data.get('daily_social_media', 0),
                        predicted_score=prediction_result.get('predicted_score', 0)
                    )
                except Exception as e:
                    # Hata durumunda sessizce devam et, kullanıcı deneyimini bozma
                    print(f"Tahmin kaydedilirken hata oluştu: {e}")
                messages.success(request, 'Tahmin başarıyla oluşturuldu!')
            else:
                messages.error(request, prediction_result.get('error', 'Tahmin oluşturulurken bir hata oluştu.'))
            
            context.update({
                'form': form,
                'prediction_result': prediction_result
            })
            return render(request, 'predictor/prediction_form.html', context)
    else:
        form = PredictionForm()
    
    context['form'] = form
    return render(request, 'predictor/prediction_form.html', context)

@csrf_exempt
def api_predict(request):
    """API tahmin endpoint'i"""
    if request.method == 'POST':
        try:
            # JSON veya form verisi olarak gönderilen istekleri kabul et
            if request.content_type == 'application/json':
                input_data = json.loads(request.body.decode('utf-8'))
            else:
                input_data = request.POST.dict()
            
            # Boş değerleri temizle
            for key in list(input_data.keys()):
                if input_data[key] == '':
                    input_data[key] = 0
            
            prediction_result = predict_performance(input_data)
            
            # Başarılı tahmin sonucunu veritabanına kaydet
            if prediction_result.get('success', False):
                try:
                    PredictionHistory.objects.create(
                        gpa=input_data.get('gpa', 0),
                        avg_exam_score=input_data.get('avg_exam_score', 0),
                        absent_rate=input_data.get('absent_rate', 0),
                        daily_study=input_data.get('daily_study', 0),
                        cram_school=input_data.get('cram_school', 'no'),
                        private_lesson=input_data.get('private_lesson', 'no'),
                        private_room=input_data.get('private_room', 'no'),
                        parent_edu=input_data.get('parent_edu', 'p'),
                        study_resources=input_data.get('study_resources', 'no'),
                        anxiety_score=input_data.get('anxiety_score', 0),
                        motivation_score=input_data.get('motivation_score', 0),
                        avg_sleep_time=input_data.get('avg_sleep_time', 0),
                        daily_social_media=input_data.get('daily_social_media', 0),
                        predicted_score=prediction_result.get('predicted_score', 0)
                    )
                except Exception as e:
                    # Hata durumunda sessizce devam et
                    print(f"API tahmin kaydedilirken hata oluştu: {e}")
            
            return JsonResponse(prediction_result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Geçersiz JSON verisi', 'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e), 'success': False}, status=400)
    else:
        return JsonResponse({'error': 'Sadece POST istekleri kabul edilir', 'success': False}, status=405)

def create_model(request):
    """Model oluşturma view'i"""
    if request.method == 'GET':
        result = create_dummy_model()
        if result.get('success', False):
            messages.success(request, "Model başarıyla oluşturuldu.")
        else:
            messages.error(request, f"Model oluşturulurken hata oluştu: {result.get('error', 'Bilinmeyen hata')}")
        
        return redirect('home')
    
    return HttpResponse("Bu sayfa sadece GET isteklerini kabul eder", status=405)

def create_sample_model_view(request):
    """Örnek model oluşturma view'i"""
    if request.method == 'GET':
        result = create_sample_model()
        if result.get('success', False):
            messages.success(request, "Örnek model başarıyla oluşturuldu.")
        else:
            messages.error(request, f"Örnek model oluşturulurken hata oluştu: {result.get('error', 'Bilinmeyen hata')}")
        
        return redirect('home')
    
    return HttpResponse("Bu sayfa sadece GET isteklerini kabul eder", status=405)

def set_language(request):
    """Dil değiştirme view'i"""
    if request.method == 'POST':
        language = request.POST.get('language', 'tr')
        
        # Session'da dil bilgisini sakla
        request.session['django_language'] = language
        
        # Geri dönülecek sayfa
        next_url = request.POST.get('next', '/')
        response = redirect(next_url)
        return response
    
    return redirect('home')