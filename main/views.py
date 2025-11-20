from django.shortcuts import render
from .prompt_generation import stream_quiz,stream_questions, stream_followup_response, stream_learning_guide, stream_lesson_plan,stream_creative_ideas, stream_realworld_examples
from django.http import JsonResponse
import json

def home(request):
    return render(request, "home.html")

def tools(request):
    tools_list = [
        {
            "title": "Lesson Plan Generator",
            "desc": "Generate a lesson plan based on a standard, topic or objective",
            "icon": "bi-journal-text",
            "url": "/tools/lesson-generator/",
            "category":"teacher"
        },
        {
            "title": "Multiple Choice Quiz / Assessment",
            "desc": "Generate a multple choice assessment, quiz or test based on any standard, topic or criteria.",
            "icon": "bi-journal-text",
            "url": "/tools/quiz/",
            "category":"teacher"
        },
        {
            "title": "Creative Ideas Generator",
            "desc": "Use our AI as a thought partner to expand on your ideas",
            "icon": "bi-magic",
            "url": "/tools/creativeIdeas-generator/",
            "category":"student"
        },

            {
            "title": "Real World Context Generator",
            "desc": "Generate Real World Examples to engage students",
            "icon": "bi-globe-americas",
            "url": "/tools/realWorldExamples-generator/",
            "category":"teacher"
        },
        # Add more tools here...
            {
            "title": "Question Generator",
            "desc": "Generate questions",
            "icon": "bi-question-diamond",
            "url": "/tools/question-generator/",
            "category":"teacher"
        },
            {
            "title": "Step by Step",
            "desc": "Generate A Step By Step guide for students to follow and learn a topic",
            "icon": "bi-book",
            "url": "/tools/learning-guide/",
            "category":"student"
        },    
    
    ]

    return render(request, "tools.html", {"tools": tools_list})

def quiz_generator(request):
    return render(request, "tools/quiz.html")

def learning_guide_generator(request):
    return render(request, "tools/learningGuide.html")
def question_generator(request):
    return render(request, "tools/questions.html")
def lesson_plan_generator(request):
    return render(request, "tools/lessonplanner.html")

def creativeIdeas_generator(request):
    return render(request, "tools/creativeIdeas.html")


def realWorldExamples_generator(request):
    return render(request, "tools/realWorldExamples.html")

def generate_stream(request):
    if request.method == 'POST':
        data = request.POST
        grade = data.get('grade')
        num_questions = data.get('num_questions')
        topic = data.get('topic')
        standard = data.get('standard')
        text = data.get('text')
        return stream_quiz(grade, num_questions, topic, standard, text)
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)
    
def generate_lesson_plan(request):
    if request.method == 'POST':
        data = request.POST
        grade = data.get('grade')
        topic = data.get('topic')
        focus_area = data.get('text')

        return stream_lesson_plan(grade, topic,focus_area)
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)
    

def generate_creative_ideas(request):
    if request.method == 'POST':
        data = request.POST
        grade = data.get('grade')
        topic = data.get('topic')

        return stream_creative_ideas(grade, topic)
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)
    
def generate_realworld_examples(request):
    if request.method == 'POST':
        data = request.POST
        grade = data.get('grade')
        topic = data.get('topic')
        focus_area = data.get('text')

        return stream_realworld_examples(grade, topic,focus_area)
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)
    
def generate_questions(request):
    if request.method == 'POST':
        data = request.POST
        grade = data.get('grade')
        num_questions = data.get('num_questions')
        topic = data.get('topic')
        difficulty = data.get('difficulty')
        return stream_questions(grade, num_questions, topic, difficulty=difficulty)
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)
    

def generate_learning_guide(request):
    if request.method == 'POST':
        data = request.POST
        grade = data.get('grade')
        topic = data.get('topic')

        return stream_learning_guide(grade, topic)
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)

def followup_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        history = data.get('history')
        message = data.get('user_message')

        # 🔁 Return a streamed response
        return stream_followup_response(history, message)
        
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)