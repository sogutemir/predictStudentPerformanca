from django import forms

class PredictionForm(forms.Form):
    gpa = forms.FloatField(
        label='GPA (Not Ortalaması)',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0-100'}),
        help_text='Öğrencinin genel not ortalaması (0-100 arası)'
    )
    
    avg_exam_score = forms.FloatField(
        label='Ortalama Sınav Puanı',
        min_value=0,
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0-500'}),
        help_text='Öğrencinin önceki sınavlardaki ortalama puanı (0-500 arası)'
    )
    
    absent_rate = forms.FloatField(
        label='Devamsızlık Oranı',
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.0-1.0'}),
        help_text='Devamsızlık oranı (0-1 arası, örneğin 0.1 = %10)'
    )
    
    daily_study = forms.IntegerField(
        label='Günlük Çalışma Süresi (Dakika)',
        min_value=0,
        max_value=1440,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dakika'}),
        help_text='Öğrencinin günlük ortalama çalışma süresi (dakika)'
    )
    
    YES_NO_CHOICES = [
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ]
    
    cram_school = forms.ChoiceField(
        label='Dershaneye Gidiyor mu?',
        choices=YES_NO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Öğrencinin bir dershaneye gidip gitmediği',
        initial='no'
    )
    
    private_lesson = forms.ChoiceField(
        label='Özel Ders Alıyor mu?',
        choices=YES_NO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Öğrencinin özel ders alıp almadığı',
        initial='no'
    )
    
    private_room = forms.ChoiceField(
        label='Kendine Ait Odası Var mı?',
        choices=YES_NO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Öğrencinin kendine ait çalışma odası olup olmadığı',
        initial='no'
    )
    
    PARENT_EDU_CHOICES = [
        ('p', 'İlkokul'),
        ('m', 'Ortaokul'),
        ('h', 'Lise'),
        ('u', 'Üniversite')
    ]
    
    parent_edu = forms.ChoiceField(
        label='Ebeveyn Eğitim Durumu',
        choices=PARENT_EDU_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Ebeveynlerin eğitim durumunun en yüksek olanı',
        initial='h'
    )
    
    study_resources = forms.ChoiceField(
        label='Yeterli Çalışma Kaynakları Var mı?',
        choices=YES_NO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Öğrencinin yeterli çalışma kaynaklarına sahip olup olmadığı',
        initial='yes'
    )
    
    anxiety_score = forms.IntegerField(
        label='Kaygı Puanı (0-10)',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-10'}),
        help_text='Öğrencinin sınav kaygısı seviyesi (0=Hiç yok, 10=Çok yüksek)',
        initial=5
    )
    
    motivation_score = forms.IntegerField(
        label='Motivasyon Puanı (0-10)',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-10'}),
        help_text='Öğrencinin motivasyon seviyesi (0=Hiç yok, 10=Çok yüksek)',
        initial=7
    )
    
    avg_sleep_time = forms.IntegerField(
        label='Ortalama Günlük Uyku Süresi (Dakika)',
        min_value=0,
        max_value=1440,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dakika (örn: 420=7 saat)'}),
        help_text='Öğrencinin günlük ortalama uyku süresi (dakika olarak, örn: 420=7 saat)',
        initial=420
    )
    
    daily_social_media = forms.IntegerField(
        label='Günlük Sosyal Medya Kullanımı (Dakika)',
        min_value=0,
        max_value=1440,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dakika'}),
        help_text='Öğrencinin günlük sosyal medya kullanım süresi (dakika)',
        initial=60
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Form alanları için daha kullanıcı dostu değerler ayarla
        if not self.is_bound:
            self.fields['gpa'].initial = 75
            self.fields['avg_exam_score'].initial = 350
            self.fields['absent_rate'].initial = 0.05
            self.fields['daily_study'].initial = 180