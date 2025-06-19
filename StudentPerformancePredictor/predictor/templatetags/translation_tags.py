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
        'Ortalama Sınav Puanı': 'Average Exam Score',
        'Öğrencinin önceki sınavlardaki ortalama puanı (0-500 arası)': "Student's average score in previous exams (0-500 range)",
        'Devamsızlık Oranı': 'Absence Rate',
        'Devamsızlık oranı (0-1 arası, örneğin 0.1 = %10)': 'Absence rate (0-1 range, e.g., 0.1 = 10%)',
        'Günlük Çalışma Süresi (Dakika)': 'Daily Study Time (Minutes)',
        'Öğrencinin günlük ortalama çalışma süresi (dakika)': "Student's daily average study time (minutes)",
        'Evet': 'Yes',
        'Hayır': 'No',
        'Dershaneye Gidiyor mu?': 'Attending Cram School?',
        'Öğrencinin bir dershaneye gidip gitmediği': 'Whether the student attends a cram school',
        'Özel Ders Alıyor mu?': 'Taking Private Lessons?',
        'Öğrencinin özel ders alıp almadığı': 'Whether the student takes private lessons',
        'Kendine Ait Odası Var mı?': 'Has Own Room?',
        'Öğrencinin kendine ait çalışma odası olup olmadığı': 'Whether the student has their own study room',
        'İlkokul': 'Primary School',
        'Ortaokul': 'Middle School',
        'Lise': 'High School',
        'Üniversite': 'University',
        'Ebeveyn Eğitim Durumu': 'Parent Education Level',
        'Ebeveynlerin eğitim durumunun en yüksek olanı': 'Highest education level of parents',
        'Yeterli Çalışma Kaynakları Var mı?': 'Has Adequate Study Resources?',
        'Öğrencinin yeterli çalışma kaynaklarına sahip olup olmadığı': 'Whether the student has adequate study resources',
        'Kaygı Puanı (0-10)': 'Anxiety Score (0-10)',
        'Öğrencinin sınav kaygısı seviyesi (0=Hiç yok, 10=Çok yüksek)': "Student's exam anxiety level (0=None, 10=Very high)",
        'Motivasyon Puanı (0-10)': 'Motivation Score (0-10)',
        'Öğrencinin motivasyon seviyesi (0=Hiç yok, 10=Çok yüksek)': "Student's motivation level (0=None, 10=Very high)",
        'Ortalama Günlük Uyku Süresi (Dakika)': 'Average Daily Sleep Duration (Minutes)',
        'Öğrencinin günlük ortalama uyku süresi (dakika olarak, örn: 420=7 saat)': "Student's daily average sleep duration (in minutes, e.g., 420=7 hours)",
        'Günlük Sosyal Medya Kullanımı (Dakika)': 'Daily Social Media Usage (Minutes)',
        'Öğrencinin günlük sosyal medya kullanım süresi (dakika)': "Student's daily social media usage time (minutes)",
        'Tahmin Et': 'Predict',
        'Tahmin Sonucu': 'Prediction Result',
        'Tahmini Üniversite Sınav Puanı': 'Predicted University Exam Score',
        'Bu puan, girilen verilere dayanarak yapılan bir tahmindir ve gerçek sonuçlar farklılık gösterebilir.': 'This score is a prediction based on the entered data and actual results may vary.',
        'Girilen Veriler:': 'Entered Data:',
        'Günlük Uyku Süresi (Dakika)': 'Daily Sleep Duration (Minutes)',
        'Kaygı Puanı': 'Anxiety Score',
        'Motivasyon Puanı': 'Motivation Score',
        # Debug için ek kontrol
        'Türkçe': 'Turkish',
        'English': 'English',
    },
    'tr': {
        # Türkçe metinler olduğu gibi kalacak
    }
}

def get_current_language_from_request(request):
    """Request'ten mevcut dili belirler"""
    if request and hasattr(request, 'GET'):
        lang = request.GET.get('lang', 'tr')
        return lang if lang in ['tr', 'en'] else 'tr'
    elif request and hasattr(request, 'session'):
        # Session'dan dil bilgisini al
        return request.session.get('django_language', 'tr')
    return 'tr'

@register.simple_tag(takes_context=True)
def trans(context, text):
    """Basit çeviri tag'i"""
    request = context.get('request')
    current_language = get_current_language_from_request(request)
    
    # Debug için log ekleyelim
    # print(f"DEBUG: Current language: {current_language}, Text: '{text}'")
    
    if current_language == 'en' and text in TRANSLATIONS['en']:
        return mark_safe(TRANSLATIONS['en'][text])
    return mark_safe(text)

@register.simple_tag(takes_context=True)
def get_current_language(context):
    """Mevcut dil kodunu döndürür"""
    request = context.get('request')
    return get_current_language_from_request(request)

@register.filter
def translate_field_label(field, request):
    """Form field label'ını çevirir"""
    if not request:
        return field.label
    
    current_language = get_current_language_from_request(request)
    if current_language == 'en' and field.label in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][field.label]
    return field.label

@register.filter
def translate_field_help_text(field, request):
    """Form field help_text'ini çevirir"""
    if not request or not field.help_text:
        return field.help_text
    
    current_language = get_current_language_from_request(request)
    if current_language == 'en' and field.help_text in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][field.help_text]
    return field.help_text

@register.simple_tag(takes_context=True)
def translate_choice(context, choice_text):
    """Select option değerlerini çevirir"""
    request = context.get('request')
    current_language = get_current_language_from_request(request)
    
    if current_language == 'en' and choice_text in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][choice_text]
    return choice_text