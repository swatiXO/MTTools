from django.shortcuts import render
from .prompt_generation import generate_preview, stream_chat_doc_response, stream_quiz,stream_questions, stream_followup_response, stream_learning_guide, stream_lesson_plan,stream_creative_ideas, stream_realworld_examples
from django.http import JsonResponse, StreamingHttpResponse
import json
from .utils.vectorStoreManager import ChatVectorManager

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
            {
            "title": "Chat With Docs",
            "desc": "Upload a document and use our AI assistant to help answer your queries",
            "icon": "bi-chat",
            "url": "/tools/chat-with-docs/",
            "category":"student"
        },  
    
    ]

    return render(request, "tools.html", {"tools": tools_list})

def quiz_generator(request):
    return render(request, "tools/quiz.html")

def chat_with_docs(request):
    return render(request, "tools/chatwithdocs.html")
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


def update_chat_history(request):
    print("Trying to update chat history")
    data = json.loads(request.body.decode('utf-8'))
    session_key = request.session.session_key
    history = data.get('history')
    message = data.get('user_message')
    vec = ChatVectorManager(chat_id=f"chat_{session_key}")
    for msg in history:
        role = msg.get('role')
        text = msg.get('content')
        vec.add_message(role, text)
        print("Added message: ", text)
    vec.add_message("user",message)
    return JsonResponse({"Success: ": "Updated Chat History"},status =200)

def followup_chat(request):
    if request.method == 'POST':
        update_chat_history(request)
        data = json.loads(request.body.decode('utf-8'))
        history = data.get('history')
        session_key = request.session.session_key
        message = data.get('user_message')
        vec = ChatVectorManager(chat_id=f"chat_{session_key}")
        similar = vec.search(message, top_k = 5)
        # 🔁 Return a streamed response
        retrieved_context = "\n".join(
            [f"{msg['role'].upper()}: {msg['text']}" for msg in similar]
        )
            # 🔁 Return a streamed response
        return stream_followup_response(retrieved_context, message)
        
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)
    


from .models import Document
from .utils.embeddings import EmbeddingManager

def stream_chat_with_doc(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data.get("user_message"))
        user_message = data.get("user_message", "")
        doc_id = data.get("doc_id")
        print(doc_id,user_message)
        if not(user_message or doc_id):
            return JsonResponse({"ERROR": "Missing message or doc_id"},status = 400)
        # doc_text = ""
        try:
            document = Document.objects.get(id=doc_id)
            # doc_text = extract_text_from_file(doc.file.path)
        except Document.DoesNotExist:
            return JsonResponse({"error": "Document not found"}, status=404)
            # doc_text = request.session.get('extracted_text',"")
        manager = EmbeddingManager(storage_key=document.storage_key)
        try:
            manager.load_or_build(document.extracted_text)
        except Exception as e:
            print("Embedding load/build error:", e)
            return JsonResponse({"status": "indexing_in_progress"}, status=202)

        return stream_chat_doc_response(request,document, user_message)


def generate_preview_with_doc(request):
    if request.method == "POST":
        doc_text = request.POST.get("doc_text", "")

        return generate_preview(request, request.session.get('extracted_text'))
