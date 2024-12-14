from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/create_question/', views.create_question, name='create_question'),
    path('question/<int:question_id>/create_answer/', views.create_answer, name='create_answer'),
]
