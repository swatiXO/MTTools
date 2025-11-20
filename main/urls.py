from django.urls import path
from .views import home, tools,quiz_generator,learning_guide_generator,generate_learning_guide, question_generator,generate_questions,generate_stream, lesson_plan_generator, generate_lesson_plan,creativeIdeas_generator,generate_creative_ideas, realWorldExamples_generator,generate_realworld_examples

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
    
    path("tools/learning-guide/generate/", generate_learning_guide, name="learning_guide_generator")
]
