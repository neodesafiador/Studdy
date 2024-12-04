#import datetime
from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import User

'''class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text'''

# Define the choices for each question
QUESTION_1_CHOICES = [
    ('A', 'Physics'),
    ('B', 'Chemistry'),
    ('C', 'Biology'),
    ('D', 'Astronomy'),
    ('E', 'Earth Science'),
    ('F', 'Environmental Science'),
    ('G', 'Anatomy'),
    ('H', 'Physical Science'),
]

QUESTION_2_CHOICES = [
    ('A', 'Reading articles or textbooks'),
    ('B', 'Watching Videos'),
    ('C', 'Doing hands-on activities or experiments'),
    ('D', 'Solving practice problems'),
]

QUESTION_3_CHOICES = [
    ('A', 'Multiple-Choice questions'),
    ('B', 'Flashcards'),
    ('C', 'Matching exercises'),
    ('D', 'Short answer questions'),
]
QUESTION_4_CHOICES = [
    ('A', 'Focus on areas I struggle with'),
    ('B', 'Provide a balanced mix of topics'),
    ('C', 'Challenge me with advanced problems'),
    ('D', 'Review basics regularly'),
]
QUESTION_5_CHOICES = [
    ('A', 'Summarizing key points in writing'),
    ('B', 'Teaching someone else'),
    ('C', 'Taking quizzes or tests'),
    ('D', 'Revisiting study materials (e.g., re-reading or re-watching content)'),
]
QUESTION_6_CHOICES = [
    ('A', 'Personal interest in the subject'),
    ('B', 'Achieving good grades or results'),
    ('C', 'Future career opportunities'),
    ('D', 'External pressure (e.g., deadlines, expectations)'),
]
QUESTION_7_CHOICES = [
    ('A', 'Break it down into smaller pieces'),
    ('B', 'Seek help from others (teachers, peers)'),
    ('C', 'Spend extra time until I understand it'),
    ('D', 'Move on and return to it later'),
]
QUESTION_8_CHOICES = [
    ('A', 'Every 25-30 minutes (Pomodoro method)'),
    ('B', 'Every 45-60 minutes'),
    ('C', 'Only when I complete a section or task'),
    ('D', 'I rarely take breaks'),
]
QUESTION_9_CHOICES = [
    ('A', 'Very Confident'),
    ('B', 'Somewhat Confident'),
    ('C', 'Neutral'),
    ('D', 'Not very confident'),
    ('E', 'Not confident at all'),
]
QUESTION_10_CHOICES = [
    ('A', 'Understanding the terminology'),
    ('B', 'Applying concepts to real-world situations'),
    ('C', 'Remembering formulas or equations'),
    ('D', 'Visualizing complex processes'),
]
class LearningProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    question_1 = models.CharField(max_length=1, choices=QUESTION_1_CHOICES)
    question_2 = models.CharField(max_length=1, choices=QUESTION_2_CHOICES)
    question_3 = models.CharField(max_length=1, choices=QUESTION_3_CHOICES)
    question_4 = models.CharField(max_length=1, choices=QUESTION_4_CHOICES)
    question_5 = models.CharField(max_length=1, choices=QUESTION_5_CHOICES)
    question_6 = models.CharField(max_length=1, choices=QUESTION_6_CHOICES)
    question_7 = models.CharField(max_length=1, choices=QUESTION_7_CHOICES)
    question_8 = models.CharField(max_length=1, choices=QUESTION_8_CHOICES)
    question_9 = models.CharField(max_length=1, choices=QUESTION_9_CHOICES)
    question_10 = models.CharField(max_length=1, choices=QUESTION_10_CHOICES)
    # Add remaining questions with appropriate choices

    def __str__(self):
        return f"{self.user.username}'s Learning Profile"

'''class UserQuestionnaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_1 = models.CharField(max_length=255)
    question_2 = models.CharField(max_length=255)
    question_3 = models.CharField(max_length=255)'''

