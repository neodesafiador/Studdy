#This code gives a home page, a login page, a signup page, and a logout page.
# Create your views here.
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
#from .forms import QuestionsForm
from .forms import LearningProfileForm
#from .models import LearningProfile
from .forms import GradeLevelSelectionForm

import openai
import os
import re
import random


# Create your views here.
# from .models import Question

def index(request):
    #Home Page
    context = {}
    return render(request, "index.html", context)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect('studdyApp:create_learning_profile')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('studdyApp:startup')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('studdyApp:startup')

def subject_detail(request, subject_name):
    # Dynamically use the subject_name to load the appropriate template
    template_name = f"{subject_name}.html"
    return render(request, template_name, {'subject_name': subject_name})

# Create Learning Profile View
@login_required
def create_learning_profile(request):
    # Check if the user already has a profile
    if hasattr(request.user, 'learningprofile'):
        return redirect('studdyApp:startup')  # Redirect to the home page if profile is complete

    if request.method == 'POST':
        form = LearningProfileForm(request.POST)
        if form.is_valid():
            q1_answer = form.cleaned_data['question_1']
            q2_answer = form.cleaned_data['question_2']
            q3_answer = form.cleaned_data['question_3']
            q4_answer = form.cleaned_data['question_4']
            q5_answer = form.cleaned_data['question_5']
            q6_answer = form.cleaned_data['question_6']
            q7_answer = form.cleaned_data['question_7']
            q8_answer = form.cleaned_data['question_8']
            q9_answer = form.cleaned_data['question_9']
            q10_answer = form.cleaned_data['question_10']

            request.session['q1_answer'] = q1_answer
            request.session['q2_answer'] = q2_answer
            request.session['q3_answer'] = q3_answer
            request.session['q4_answer'] = q4_answer
            request.session['q5_answer'] = q5_answer
            request.session['q6_answer'] = q6_answer
            request.session['q7_answer'] = q7_answer
            request.session['q8_answer'] = q8_answer
            request.session['q9_answer'] = q9_answer
            request.session['q10_answer'] = q10_answer

            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('studdyApp:startup')  # Redirect to home or dashboard after completion
    else:
        form = LearningProfileForm()
    return render(request, 'create_learning_profile.html', {'form': form})

# This is the view for users to select what grade level they are. This will appear each time they go to a subject
def select_subject_grade(request, subject_name):
    if request.method == 'POST':
        form = GradeLevelSelectionForm(request.POST, subject=subject_name)  # Pass subject to form
        if form.is_valid():
            grade_level = form.cleaned_data['grade_level']
            return redirect(f'/{grade_level}_{subject_name.replace(" ", "_").lower()}/')
    else:
        form = GradeLevelSelectionForm(subject=subject_name)  # Pass subject to form

    # Replace underscores with spaces for display in the template
    display_subject_name = subject_name.replace("_", " ")

    return render(request, 'select_subject_grade.html', {
        'form': form,
        'subject_name': display_subject_name

    #return render(request, 'select_subject_grade.html', {'form': form, 'subject_name': subject_name})
})

# Recommend System using GPT
def recommend_problems(request, subject_choice, grade_choice, feedback="", practice_type='multiple-choice questions'):
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    q3_answer = request.session.get('q3_answer', '')
    q4_answer = request.session.get('q4_answer', '')
    q5_answer = request.session.get('q5_answer', '')
    q6_answer = request.session.get('q6_answer', '')
    q7_answer = request.session.get('q7_answer', '')
    q9_answer = request.session.get('q9_answer', '')
    q10_answer = request.session.get('q10_answer', '')

    practice_types = {
        'A': 'multiple-choice questions',
        'B': 'flashcards',
        'C': 'matching exercises',
        'D': 'short answer questions',
    }
    practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

    number_question = 10

    prompt = f"""
Based on the following student profile, generate {number_question} {practice_type} that are appropriate for their grade and subject interest. Tailor the practice materials according to their preferences and needs.

Student Profile:
- Interested Subject: {subject_choice} at the {grade_choice} level
- Answers to the questionnaire:
    1. Would you like to receive more practice problems in areas you are struggling with, or would you prefer a balanced approach?
       Answer: {q4_answer}
    2. How do you prefer to review what you’ve learned?
       Answer: {q5_answer}
    3. What motivates you to study?
       Answer: {q6_answer}
    4. How do you handle challenging concepts?
       Answer: {q7_answer}
    5. How confident are you in solving math-related problems in science subjects?
       Answer: {q9_answer}
    6. What do you find most challenging about learning new scientific concepts?
        Answer: {q10_answer}

Please provide only the practice materials; do not include explanations or solutions.
"""

    if practice_type == 'flashcards':
        prompt += "\n\nPlease format the flashcards as follows:\n\nQuestion: [Your question here]\nAnswer: [Your answer here]\n\nSeparate each flashcard with a blank line."
    elif practice_type == 'multiple-choice questions':
        prompt += """

Please format the multiple-choice questions as follows:

Question 1: [Your question here]
A. Option A
B. Option B
C. Option C
D. Option D

Question 2: [Your question here]
A. Option A
B. Option B
C. Option C
D. Option D

... (continue for all questions)

At the end, list the correct answers in the following format:

Correct Answer:
1. [Option Letter]
2. [Option Letter]
3. [Option Letter]
...

**Important Instructions:**

- Do **not** make the correct answers follow any predictable pattern.

- Do **not** include any explanations or additional text.

- **Strictly** follow this format.
"""

    elif practice_type == 'matching exercises':
        prompt += """

Please generate matching exercises as follows:

- Provide two lists:
  - **List A**: A list of terms or concepts.
  - **List B**: A list of definitions or descriptions.

- Ensure that each item in List A matches one item in List B.

- Randomize the order of items in both lists.

- Format the output as:

List A:
1. Term A1
2. Term A2
3. Term A3
...

List B:
A. Definition B1
B. Definition B2
C. Definition B3
...

At the end, provide the correct matches in the following format:

Answer Key:
1 - [Letter]
2 - [Letter]
3 - [Letter]
...

**Important Instructions:**

- Do **not** include any explanations or additional text.

- Ensure the matches are correct and that the items are appropriately randomized.

- **Strictly** follow this format.
"""

    elif practice_type == 'short answer questions':
        prompt += f"""
- List all the questions first.

- Then, provide the answers separately in the same order.

Format:

Questions:
1. [Question 1]

2. [Question 2]

...

{number_question}. [Question {number_question}]

Answers:
1. [Answer to Question 1]

2. [Answer to Question 2]

...

{number_question}. [Answer to Question {number_question}]

**Important Instructions:**

- Do not include any explanations or additional text.

- Ensure questions cover a range of topics within {subject_choice}.

- The answers should be brief, typically one or two sentences.

- Strictly follow the format to facilitate parsing.
"""


    if feedback:
        prompt += f" The student provided the following feedback on the previous set of questions: '{feedback}'. Please adjust the new questions accordingly."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that generates educational practice materials for students."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            n=1,
            temperature=0.7,
        )

        generated_problems = response['choices'][0]['message']['content']
        if practice_type == 'flashcards':
            flashcards = []
            flashcard_texts = generated_problems.strip().split('\n\n')
            for flashcard_text in flashcard_texts:
                lines = flashcard_text.strip().split('\n')
                question_line = next((line for line in lines if line.startswith('Question:')), '')
                answer_line = next((line for line in lines if line.startswith('Answer:')), '')
                question = question_line[len('Question:'):].strip()
                answer = answer_line[len('Answer:'):].strip()
                flashcards.append({'question': question, 'answer': answer})
            return flashcards

        elif practice_type == 'multiple-choice questions':
            try:
                # Split questions and answers
                parts = generated_problems.strip().split('Correct Answer:')
                if len(parts) < 2:
                    return "Error: 'Correct Answer:' not found in the generated problems."

                questions_part = parts[0].strip()
                answers_part = parts[1].strip()

                # Parse questions
                question_blocks = re.findall(r'(Question \d+:.*?(?=Question \d+:|$))', questions_part, re.DOTALL)

                if not question_blocks:
                    return "Error: No questions found in the generated problems."

                questions = []
                for block in question_blocks:
                    lines = block.strip().split('\n')
                    question_line = lines[0]
                    options = lines[1:]
                    question_number = re.search(r'Question (\d+):', question_line).group(1)
                    question_text = re.sub(r'^Question \d+:', '', question_line).strip()
                    options_dict = {}
                    for option_line in options:
                        match = re.match(r'^([A-D])\.\s+(.*)', option_line.strip())
                        if match:
                            option_letter = match.group(1)
                            option_text = match.group(2)
                            options_dict[option_letter] = option_text
                    questions.append({
                        'number': question_number,
                        'question': question_text,
                        'options': options_dict
                    })

                # Parse answers
                answer_lines = answers_part.strip().split('\n')
                correct_answers = {}
                for line in answer_lines:
                    match = re.match(r'^(\d+)\.\s*([A-D])', line.strip())
                    if match:
                        number = match.group(1)
                        letter = match.group(2)
                        correct_answers[number] = letter

                # Combine questions and correct answers
                # for q in questions:
                #     q['answer'] = correct_answers.get(q['number'], '')
                for q in questions:
                    # Assign a random correct answer from A, B, C, D
                    random_choices = ['A', 'B', 'C', 'D']
                    new_correct_letter = random.choice(random_choices)
                    old_correct_letter = correct_answers.get(q['number'], '')

                    # Swap texts between the old and new correct letters
                    if old_correct_letter != new_correct_letter:
                        # Get the correct text and the text currently at the new correct letter
                        correct_text = q['options'][old_correct_letter]
                        incorrect_text = q['options'][new_correct_letter]

                        # Swap the texts
                        q['options'][old_correct_letter] = incorrect_text
                        q['options'][new_correct_letter] = correct_text

                    # Update correct_answers dictionary
                    correct_answers[q['number']] = new_correct_letter

                    # Rearrange options to A, B, C, D order
                    sorted_options = {key: q['options'][key] for key in ['A', 'B', 'C', 'D'] if key in q['options']}
                    q['options'] = sorted_options

                # Update the questions with their randomized correct answers
                for q in questions:
                    q['answer'] = correct_answers.get(q['number'], '')

                return questions

            except Exception as e:
                return f"An error occurred while processing multiple-choice questions: {str(e)}"

        elif practice_type == 'matching exercises':
            try:
                # Extract List A, List B, and Answer Key
                list_a_match = re.search(r'List A:\s*(.*?)\s*List B:', generated_problems, re.DOTALL)
                list_b_match = re.search(r'List B:\s*(.*?)\s*Answer Key:', generated_problems, re.DOTALL)
                answer_key_match = re.search(r'Answer Key:\s*(.*)', generated_problems, re.DOTALL)

                if not (list_a_match and list_b_match and answer_key_match):
                    return "Error parsing matching exercises"

                list_a_text = list_a_match.group(1).strip()
                list_b_text = list_b_match.group(1).strip()
                answer_key_text = answer_key_match.group(1).strip()

                # Parse List A
                list_a_items = re.findall(r'(\d+)\.\s+(.*)', list_a_text)
                list_a = [{'number': num.strip(), 'term': term.strip()} for num, term in list_a_items]

                # Parse List B
                list_b_items = re.findall(r'([A-Z])\.\s+(.*)', list_b_text)
                list_b = [{'letter': letter.strip(), 'definition': definition.strip()} for letter, definition in list_b_items]

                # Parse Answer Key
                answer_key_lines = answer_key_text.strip().split('\n')
                answer_key = {}
                for line in answer_key_lines:
                    match = re.match(r'^(\d+)\s*-\s*([A-Z])', line.strip())
                    if match:
                        num = match.group(1).strip()
                        letter = match.group(2).strip()
                        answer_key[num] = letter

                # Combine into a data structure
                matching_exercise = {
                    'list_a': list_a,
                    'list_b': list_b,
                    'answer_key': answer_key
                }

                return matching_exercise

            except Exception as e:
                return f"An error occurred while processing matching exercises: {str(e)}"

        elif practice_type == 'short answer questions':
            try:
                # Split into Questions and Answers
                parts = re.split(r'Answers:', generated_problems.strip())
                if len(parts) < 2:
                    return "Error: 'Answers:' section not found in the generated problems."

                questions_part = parts[0].strip()
                answers_part = parts[1].strip()

                # Parse Questions
                question_lines = re.findall(r'\d+\.\s+(.*)', questions_part)
                questions = [{'number': idx + 1, 'question': q.strip()} for idx, q in enumerate(question_lines)]

                # Parse Answers
                answer_lines = re.findall(r'\d+\.\s+(.*)', answers_part)
                for idx, a in enumerate(answer_lines):
                    if idx < len(questions):
                        questions[idx]['answer'] = a.strip()

                return questions

            except Exception as e:
                return f"An error occurred while processing short answer questions: {str(e)}"


        else:
            return generated_problems

    except Exception as e:
        return f"An error occurred while generating problems: {str(e)}"


def grade_answers(problems, user_answers):
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    graded_results = []

    for problem in problems:
        question_number = str(problem['number'])
        user_answer = user_answers.get(question_number, '').strip()
        correct_answer = problem['answer']

        # Check if the user's answer is empty
        if not user_answer:
            graded_results.append({
                'number': question_number,
                'question': problem['question'],
                'correct_answer': correct_answer,
                'user_answer': user_answer,
                'score': 0,
                'feedback': "No answer provided."
            })
            continue  # Proceed to the next question

        # Prepare the grading prompt
        grading_prompt = f"""
You are to grade the following student's answer on a scale from 0 to 5, where 5 is the highest score. Base the score on accuracy, completeness, and understanding.

- If the student's answer is empty, blank, or irrelevant to the question, assign a score of 0.

- Provide the evaluation in the following format:
Score: [An integer from 0 to 5]
Feedback: [One sentence of feedback]

Question: {problem['question']}

Correct Answer: {correct_answer}

Student's Answer: {user_answer}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a strict but fair grader. Provide only the score and feedback as instructed."},
                    {"role": "user", "content": grading_prompt}
                ],
                max_tokens=150,
                n=1,
                temperature=0,
            )

            grading_output = response['choices'][0]['message']['content'].strip()

            # Parse the score and feedback
            score_match = re.search(r'Score:\s*(\b[0-5]\b)', grading_output)
            feedback_match = re.search(r'Feedback:\s*(.*)', grading_output)

            if score_match:
                score = int(score_match.group(1))
            else:
                score = 0  # Default to 0 if parsing fails

            if feedback_match:
                feedback = feedback_match.group(1).strip()
            else:
                feedback = "No feedback provided."

            graded_results.append({
                'number': question_number,
                'question': problem['question'],
                'correct_answer': correct_answer,
                'user_answer': user_answer,
                'score': score,
                'feedback': feedback,
            })

        except Exception as e:
            graded_results.append({
                'number': question_number,
                'question': problem['question'],
                'correct_answer': correct_answer,
                'user_answer': user_answer,
                'score': 0,
                'feedback': f"An error occurred while grading: {str(e)}",
            })

    return graded_results


# Making a view for each grade level of each subject

def ninth_physical_science(request):
    subject_choice = 'Physical Science'
    grade_choice = '9th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        # Handle grading of user answers
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        # Retrieve the original questions and correct answers
        problems = request.session.get('problems', [])

        # Grade the user's answers using OpenAI
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        # Handle initial problem generation or feedback submission
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems  # Store problems in session for grading

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '9th_physical_science.html', context)


def ninth_biology(request):
    subject_choice = 'Biology'
    grade_choice = '9th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '9th_biology.html', context)


def tenth_biology(request):
    subject_choice = 'Biology'
    grade_choice = '10th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '10th_biology.html', context)


def eleventh_biology(request):
    subject_choice = 'Biology'
    grade_choice = '11th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '11th_biology.html', context)


def twelfth_biology(request):
    subject_choice = 'Biology'
    grade_choice = '12th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '12th_biology.html', context)


def tenth_chemistry(request):
    subject_choice = 'Chemistry'
    grade_choice = '10th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '10th_chemistry.html', context)


def eleventh_chemistry(request):
    subject_choice = 'Chemistry'
    grade_choice = '11th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '11th_chemistry.html', context)


def tenth_earth_science(request):
    subject_choice = 'Earth Science'
    grade_choice = '10th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '10th_earth_science.html', context)


def ninth_environmental_science(request):
    subject_choice = 'Environmental Science'
    grade_choice = '9th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '9th_environmental_science.html', context)


def twelfth_environmental_science(request):
    subject_choice = 'Environmental Science'
    grade_choice = '12th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '12th_environmental_science.html', context)


def twelfth_astronomy(request):
    subject_choice = 'Astronomy'
    grade_choice = '12th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '12th_astronomy.html', context)


def ninth_anatomy(request):
    subject_choice = 'Anatomy'
    grade_choice = '9th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '9th_anatomy.html', context)


def tenth_anatomy(request):
    subject_choice = 'Anatomy'
    grade_choice = '10th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '10th_anatomy.html', context)


def eleventh_anatomy(request):
    subject_choice = 'Anatomy'
    grade_choice = '11th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '11th_anatomy.html', context)


def twelfth_anatomy(request):
    subject_choice = 'Anatomy'
    grade_choice = '12th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '12th_anatomy.html', context)


def eleventh_physics(request):
    subject_choice = 'Physics'
    grade_choice = '11th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '11th_physics.html', context)


def twelfth_physics(request):
    subject_choice = 'Physics'
    grade_choice = '12th'

    q3_answer = request.session.get('q3_answer', '')
    feedback = ''

    if request.method == 'POST' and 'submit_answers' in request.POST:
        user_answers = {}
        for key in request.POST:
            if key.startswith('user_answer_'):
                question_number = key[len('user_answer_'):]
                user_answers[question_number] = request.POST[key]

        problems = request.session.get('problems', [])
        graded_results = grade_answers(problems, user_answers)

        context = {
            'q3_answer': q3_answer,
            'practice_type': 'short answer questions',
            'graded_results': graded_results,
            'feedback': feedback,
        }

    else:
        if request.method == 'POST':
            q3_answer = request.POST.get('q3_answer', q3_answer)
            request.session['q3_answer'] = q3_answer
            feedback = request.POST.get('feedback', '')

        practice_types = {
            'A': 'multiple-choice questions',
            'B': 'flashcards',
            'C': 'matching exercises',
            'D': 'short answer questions',
        }
        practice_type = practice_types.get(q3_answer, 'multiple-choice questions')

        problems = recommend_problems(request, subject_choice, grade_choice, feedback, practice_type)
        request.session['problems'] = problems

        context = {
            'q3_answer': q3_answer,
            'practice_type': practice_type,
            'problems': problems,
            'feedback': feedback,
        }
    return render(request, '12th_physics.html', context)




