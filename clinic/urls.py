from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("index/<str:doctor_img_name>", views.index, name="index"),
    path("schedule", views.get_schedule, name="schedule"),
    path("contacts", views.get_contacts, name="contacts"),
    path("vacancy", views.get_vacancy, name="vacancy"),
    path("staff", views.get_staff, name="staff"),
    path("reviews/<str:doctor_ln>", views.get_reviews, name="reviews"),
    path("making-an-appointment", views.get_appointment_page, name="making-an-appointment"),
    path("registration", views.get_registration_form, name="registration"),
    path("register", views.validate_registration, name="register"),
    path("send_contract_num", views.send_contract_num, name="send_contract_num"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("sendReview", views.send_review, name="send_review")
]
