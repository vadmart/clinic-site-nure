from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("staff", views.staff, name="staff"),
    path("schedule", views.schedule, name="schedule"),
    path("contacts", views.contacts, name="contacts"),
    path("vacancy", views.vacancy, name="vacancy"),
    path("reviews/<int:doctor_id>", views.reviews, name="reviews"),
    path("making-an-appointment", views.make_appointment, name="make_appointment"),
    path("making-a-contract", views.contract_page, name="make_contract"),
    path("doctor-info", views.doctor_info, name="doctor_info"),
    path("doctor_lfp", views.doctor_lfp, name="doctor_lfp"),
    path("record", views.record, name="record"),
    # path("code-submitting", views.code_submitting, name="code-submitting"),
    path("reviews/check-person", views.check_person, name="check_person"),
    path("reviews/<int:doctor_id>/send", views.add_review, name="add_review")
]
