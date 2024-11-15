#Here are the forms that the user will be given to fill out when
#they are either signing up or logging into the app.


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .models import UserQuestionnaire
from .models import LearningProfile, QUESTION_1_CHOICES, QUESTION_2_CHOICES, QUESTION_3_CHOICES
from .models import QUESTION_4_CHOICES, QUESTION_5_CHOICES, QUESTION_6_CHOICES, QUESTION_7_CHOICES, QUESTION_8_CHOICES
from .models import QUESTION_9_CHOICES, QUESTION_10_CHOICES


#uses built in user creation form from django to have the user create
#their account.
#Asks for username, password, and password confirmation
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

'''class QuestionsForm(forms.ModelForm):
    class Meta:
        model = UserQuestionnaire
        fields = ['question_1', 'question_2', 'question_3']  # Customize fields as needed'''

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Here's where you add the class to the widget
        self.fields['username'].widget.attrs.update({'class': 'input-box'})
        self.fields['password'].widget.attrs.update({'class': 'input-box'})



class LearningProfileForm(forms.ModelForm):
    # First question as a dropdown for subject choice
    question_1 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_1_CHOICES),
    label="Which subject are you most interested in studying right now?", widget=forms.Select())
    question_2 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_2_CHOICES),
    label="How do you prefer to learn new information?", widget=forms.Select())
    question_3 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_3_CHOICES),
    label="What type of practice helps you learn the best?", widget=forms.Select())
    question_4 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_4_CHOICES),
    label="Would you like to receive more practice problems in areas you are struggling with, or would you prefer a balanced approach?",
    widget=forms.Select())
    question_5 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_5_CHOICES),
    label="How do you prefer to review what you’ve learned?", widget=forms.Select())
    question_6 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_6_CHOICES),
    label="What motivates you to study?", widget=forms.Select())
    question_7 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_7_CHOICES),
    label="How do you handle challenging concepts?", widget=forms.Select())
    question_8 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_8_CHOICES),
    label="How often do you prefer to take breaks during study sessions?", widget=forms.Select())
    question_9 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_9_CHOICES),
    label="How confident are you in solving math-related problems in science subjects?", widget=forms.Select())
    question_10 = forms.ChoiceField(
    choices=[('', 'Select a subject')] + list(QUESTION_10_CHOICES),
    label="What do you find most challenging about learning new scientific concepts?", widget=forms.Select())

    class Meta:
        model = LearningProfile
        fields = ['question_1', 'question_2', 'question_3', 'question_4',
        'question_5', 'question_6', 'question_7', 'question_8', 'question_9', 'question_10']


# Form for users to select their grade level
class GradeLevelSelectionForm(forms.Form):
    GRADE_CHOICES = [
        (9, '9th Grade'),
        (10, '10th Grade'),
        (11, '11th Grade'),
        (12, '12th Grade'),
    ]

    grade_level = forms.ChoiceField(label='Select Grade Level', choices=GRADE_CHOICES)

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)  # Get subject from kwargs
        super().__init__(*args, **kwargs)

        # Modify choices based on subject
        if subject:
            if subject == 'physical_science':
                self.fields['grade_level'].choices = [(9, '9th Grade')]
            elif subject == 'earth_science':
                self.fields['grade_level'].choices = [(10, '10th Grade')]
            elif subject == 'environmental_science':
                self.fields['grade_level'].choices = [(9, '9th Grade'), (12, '12th Grade')]
            elif subject == 'chemistry':
                self.fields['grade_level'].choices = [(10, '10th Grade'), (11, '11th Grade')]
            elif subject == 'physics':
                self.fields['grade_level'].choices = [(11, '11th Grade'), (12, '12th Grade')]
            elif subject == 'astronomy':
                self.fields['grade_level'].choices = [(12, '12th Grade')]
            else:
                # For anatomy and biology, show all grades
                self.fields['grade_level'].choices = self.GRADE_CHOICES


