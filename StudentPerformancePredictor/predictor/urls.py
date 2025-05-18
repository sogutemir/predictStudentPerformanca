from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tahmin/', views.prediction_form, name='prediction_form'),
    path('api/tahmin/', views.api_predict, name='api_predict'),
    path('model/create/', views.create_model, name='create_model'),
    path('model/create-sample/', views.create_sample_model_view, name='create_sample_model'),
] 