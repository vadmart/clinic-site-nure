from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz),
    path("get-questions", views.questions)
]
