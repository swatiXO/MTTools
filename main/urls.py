from django.urls import path
from .views import chat_with_docs, generate_preview_with_doc, home, stream_chat_with_doc, tools,quiz_generator,followup_chat,learning_guide_generator,generate_learning_guide, question_generator,generate_questions,generate_stream, lesson_plan_generator, generate_lesson_plan,creativeIdeas_generator,generate_creative_ideas, realWorldExamples_generator,generate_realworld_examples
from .utils.documentUtils import upload_document
urlpatterns = [
    path("", home, name="home"),
    path("tools/", tools, name="tools"),
    path("tools/quiz/", quiz_generator, name="quiz_generator"),
    path("tools/quiz/generate/",generate_stream , name="quiz_generator"),


    path("tools/lesson-generator/", lesson_plan_generator, name="lesson_plan_generator"),
    path("tools/lesson-generator/generate/", generate_lesson_plan, name="lesson_plan_generator"),

    path("tools/creativeIdeas-generator/", creativeIdeas_generator, name="creative_idea_generator"),
    path("tools/creativeIdeas-generator/generate/", generate_creative_ideas, name="creative_idea_generator"),

    path("tools/realWorldExamples-generator/", realWorldExamples_generator, name="realworld_generator"),
    path("tools/realWorldExamples-generator/generate/", generate_realworld_examples, name="realworld_generator"),

    
    path("tools/question-generator/", question_generator, name="question_generator"),
    path("tools/question-generator/generate/", generate_questions, name="question_generator"),



    path("tools/learning-guide/", learning_guide_generator, name="learning_guide_generator"),
    
    path("tools/learning-guide/generate/", generate_learning_guide, name="learning_guide_generator"),
    path("chat_followup/", followup_chat, name="followup_chat"),

    path("tools/chat-with-docs/", chat_with_docs, name="chat_with_docs"),
    path("tools/chat-with-docs/upload/", upload_document, name="upload_chat_with_docs"),
    path("tools/chat-with-docs/generate_preview/", generate_preview_with_doc, name="chat_with_docs"),
    path("chat_with_docs_followup/", stream_chat_with_doc, name="chat_with_docs"),

]
