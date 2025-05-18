from django.db import models
from django.utils import timezone

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    grade = models.IntegerField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performances')
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    exam_date = models.DateField()
    
    def __str__(self):
        return f"{self.student.first_name}'s {self.subject} performance: {self.score}"

class PredictionHistory(models.Model):
    """Tahmin geçmişini tutmak için kullanılır."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    prediction_date = models.DateTimeField(default=timezone.now)
    
    # Girdi değerleri
    gpa = models.FloatField()
    avg_exam_score = models.FloatField()
    absent_rate = models.FloatField()
    daily_study = models.IntegerField()
    cram_school = models.CharField(max_length=5)
    private_lesson = models.CharField(max_length=5)
    private_room = models.CharField(max_length=5)
    parent_edu = models.CharField(max_length=2)
    study_resources = models.CharField(max_length=5)
    anxiety_score = models.IntegerField()
    motivation_score = models.IntegerField()
    avg_sleep_time = models.IntegerField()
    daily_social_media = models.IntegerField()
    
    # Çıktı değeri
    predicted_score = models.FloatField()
    
    def __str__(self):
        if self.student:
            return f"{self.student.first_name}'s prediction on {self.prediction_date.strftime('%Y-%m-%d')}: {self.predicted_score}"
        return f"Anonim tahmin ({self.prediction_date.strftime('%Y-%m-%d')}): {self.predicted_score}"
