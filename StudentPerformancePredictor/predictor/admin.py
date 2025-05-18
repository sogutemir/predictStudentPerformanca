from django.contrib import admin
from .models import Student, Performance, PredictionHistory

# Admin panel özelleştirmeleri
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id', 'grade')
    search_fields = ('first_name', 'last_name', 'student_id')
    list_filter = ('grade',)

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'exam_date')
    list_filter = ('subject', 'exam_date')
    search_fields = ('student__first_name', 'student__last_name', 'subject')
    date_hierarchy = 'exam_date'

class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'prediction_date', 'predicted_score', 'gpa', 'avg_exam_score')
    list_filter = ('prediction_date', 'cram_school', 'private_lesson', 'parent_edu')
    search_fields = ('student__first_name', 'student__last_name')
    date_hierarchy = 'prediction_date'
    readonly_fields = ('prediction_date', 'predicted_score')

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(PredictionHistory, PredictionHistoryAdmin)
