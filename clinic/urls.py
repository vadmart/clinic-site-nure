from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("schedule", views.get_schedule, name="schedule"),
    path("contacts", views.get_contacts, name="contacts"),
    path("vacancy", views.get_vacancy, name="vacancy"),
    path("staff", views.DoctorList.as_view(), name="staff"),
    path("reviews/<slug:doctor_slug>", views.DoctorReviews.as_view(), name="reviews"),
    path("making-an-appointment", login_required(views.AppointmentForm.as_view()), name="making-an-appointment"),
    path("record", views.AppointmentForm.as_view(), name="record"),
    path("registration", views.get_registration_form, name="registration"),
    path("register", views.validate_registration, name="register"),
    path("send_contract_num", views.send_contract_num, name="send_contract_num"),
    path("user-cabinet", login_required(views.UserCabinet.as_view()), name="user-cabinet"),
    path("sendReview", views.SendReview.as_view(), name="send_review"),
    path("<str:doctor_img_name>", views.index, name="index")
]
