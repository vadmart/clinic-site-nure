from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("schedule", views.get_schedule, name="schedule"),
    path("contacts", views.get_contacts, name="contacts"),
    path("vacancy", views.get_vacancy, name="vacancy"),
    path("staff", views.DoctorList.as_view(), name="staff"),
    path("reviews/<slug:doctor_slug>", views.DoctorReviews.as_view(), name="reviews"),
    path("making-an-appointment", views.get_appointment_page, name="making-an-appointment"),
    path("record", views.get_appointment_page, name="record"),
    path("registration", views.get_registration_form, name="registration"),
    path("register", views.validate_registration, name="register"),
    path("send_contract_num", views.send_contract_num, name="send_contract_num"),
    path("login", LoginView.as_view(), name="login"),
    path("user-cabinet", views.UserCabinet.as_view(), name="user-cabinet"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("sendReview", views.SendReview.as_view(), name="send_review"),
    path("<str:doctor_img_name>", views.index, name="index")
]
