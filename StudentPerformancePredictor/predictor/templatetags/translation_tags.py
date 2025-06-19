from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Basit çeviri sözlüğü
TRANSLATIONS = {
    'en': {
        'Öğrenci Performans Tahmincisi': 'Student Performance Predictor',
        'Ana Sayfa': 'Home',
        'Performans Tahmini': 'Performance Prediction',
        'Bu uygulama, öğrenci verilerini analiz ederek üniversite sınav puanlarını tahmin etmeye yardımcı olur.': 'This application helps predict university exam scores by analyzing student data.',
        'Öğrenci bilgilerini girerek gelecekteki üniversite sınav performansını tahmin edebilirsiniz.': 'You can predict future university exam performance by entering student information.',
        'Başlayın': 'Get Started',
        'Model İstatistikleri': 'Model Statistics',
        'Linear Regression modelimizin performans istatistikleri': 'Performance statistics of our Linear Regression model',
        'Tahmin Doğruluğu': 'Prediction Accuracy',
        'Ortalama tahmin başarısı': 'Average prediction success',
        'Ortalama kare hatanın karekökü': 'Root Mean Square Error',
        'R² Değeri': 'R² Value',
        'Belirleme katsayısı': 'Coefficient of determination',
        'Değişken Sayısı': 'Number of Variables',
        'Modelde kullanılan özellik sayısı': 'Number of features used in the model',
        'Öğrenci Performans Tahmini': 'Student Performance Prediction',
        'GPA (Not Ortalaması)': 'GPA (Grade Point Average)',
        'Öğrencinin genel not ortalaması (0-100 arası)': "Student's overall grade point average (0-100 range)",
    },
    'tr': {
        # Türkçe metinler olduğu gibi kalacak
    }
}

@register.simple_tag(takes_context=True)
def trans(context, text):
    """Basit çeviri tag'i"""
    request = context.get('request')
    if request:
        language = request.session.get('language', 'tr')
        if language == 'en' and text in TRANSLATIONS['en']:
            return mark_safe(TRANSLATIONS['en'][text])
    return mark_safe(text)

@register.simple_tag(takes_context=True)
def get_current_language(context):
    """Mevcut dil kodunu döndürür"""
    request = context.get('request')
    if request:
        return request.session.get('language', 'tr')
    return 'tr' 