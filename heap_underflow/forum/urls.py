from django.urls import path
from .views import AnswerDeleteView, QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView
from . import views

urlpatterns = [
    path('', QuestionListView.as_view(), name='forum-home'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('question/new/', QuestionCreateView.as_view(), name='question-create'),
    path('question/<int:pk>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),
    path('question/<int:q_pk>/answer/<int:a_pk>/delete/', AnswerDeleteView.as_view(), name='answer-delete'),
    path('about/', views.about, name='forum-about'),
]
