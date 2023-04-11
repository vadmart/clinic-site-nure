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
    path("login", views.get_login_form, name="login"),
    path("registration", views.get_registration_form, name="registration"),
    path("validate_registration", views.validate_registration, name="validate_registration"),
    path("validate_login", views.validate_login, name="validate_login"),
    path("send_contract_num", views.send_contract_num, name="send_contract_num")
]
