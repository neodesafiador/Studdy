from django.contrib import admin

# Register your models here.
# from .models import Question
from .models import LearningProfile

class LearningProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'question_7', 'question_8', 'question_9', 'question_10')

admin.site.register(LearningProfile, LearningProfileAdmin)

# admin.site.register(Question)