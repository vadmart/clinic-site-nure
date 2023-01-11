from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("staff", views.staff, name="staff"),
    path("schedule", views.schedule, name="schedule"),
    path("contacts", views.contacts, name="contacts"),
    path("vacancy", views.vacancy, name="vacancy"),
    path("reviews", views.reviews, name="reviews"),
    path("making-an-appointment", views.make_appointment, name="make_appointment"),
    path("quiz", views.quiz, name="quiz")
]
