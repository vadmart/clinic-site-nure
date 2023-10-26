import datetime

from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, View
from .forms import ReviewForm

from clinic.models import Doctor, Patient, Recording, Schedule
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from clinic.contract import get_rand_contract_num
from clinic.turbosms import TurboSMSMessage
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import json


# Create your views here.
def index(request, doctor_img_name="default_photo"):
    return render(request, template_name="clinic/index.html", context={"doctor_img_name": doctor_img_name})


def get_schedule(request):
    return render(request, template_name="clinic/pages/schedule-work.html")


def get_contacts(request):
    return render(request, template_name="clinic/pages/contacts.html")


def get_vacancy(request):
    return render(request, template_name="clinic/pages/vacancy.html")


def quiz(request):
    return render(request, template_name="clinic/pages/", context={"lang": request.LANGUAGE_CODE})


class DoctorList(ListView):
    model = Doctor
    template_name = "clinic/pages/staff.html"
    context_object_name = "doctors"


class DoctorReviews(DetailView):
    model = Doctor
    template_name = "clinic/pages/reviews.html"
    context_object_name = "doctor"
    slug_url_kwarg = "doctor_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            context["form"] = ReviewForm(initial={
                "doctor": self.get_object(),
                "patient": self.request.user.patient
            })
        return context


class SendReview(CreateView):
    model = Doctor
    form_class = ReviewForm
    template_name = "clinic/pages/reviews.html"
    context_object_name = "doctor"
    slug_url_kwarg = "doctor_slug"


class AppointmentForm(View):
    def get(self, request):
        try:
            doctor = Patient.objects.get(user=request.user).doctor
            appointments = sorted(doctor.schedule_set.filter(recording=None,
                                                             start_datetime__gt=datetime.datetime.now()))
            return render(request,
                          template_name="clinic/pages/making-an-appointment.html",
                          context={"doctor": doctor,
                                   "appointments": appointments,
                                   "app_dates": get_appointments_dates(appointments)})
        except Patient.DoesNotExist:
            doctor_err = _(
                "Помилка: не знайдено лікаря, із яким узгоджено контракт. Перевірте свій акаунт або перезавантажте сторінку!")
            return render(request,
                          template_name="clinic/pages/making-an-appointment.html",
                          context={"doctor_err": doctor_err})

    def post(self, request):
        doctor = Doctor.objects.get(pk=request.POST["appointment_doctor_pk"])
        recording = Recording(person=request.user.patient,
                              health_complaint=request.POST["appointment_complaint"])
        recording.save()
        time = get_full_time(request.POST["appointment_time"]) if request.LANGUAGE_CODE.lower() == "en" else \
            request.POST["appointment_time"]
        dt_tm = datetime.datetime.strptime(request.POST["appointment_date"] + "T" + time, "%d.%m.%YT%H:%M")
        try:
            schedule = Schedule.objects.get(doctor=doctor,
                                            start_datetime=dt_tm)
            schedule.recording = recording
            schedule.save()
            appointments = sorted(doctor.schedule_set.filter(recording=None,
                                                             start_datetime__gt=datetime.datetime.now()))
            return render(request,
                          template_name="clinic/pages/making-an-appointment.html",
                          context={"doctor": doctor,
                                   "appointments": appointments,
                                   "app_dates": get_appointments_dates(appointments),
                                   "success_message": _(
                                       "Запис на прийом успішно виконано! За необхідністю можете записатися ще")})
        except ValidationError:
            err = "Помилка: цей час вже зайнято, перезавантажте сторінку та оберіть інший"
            appointments = sorted(doctor.schedule_set.filter(recording=None,
                                                             start_datetime__gt=datetime.datetime.now()))
            return render(request,
                          template_name="clinic/pages/making-an-appointment.html",
                          context={"doctor": doctor,
                                   "appointments": appointments,
                                   "app_dates": get_appointments_dates(appointments),
                                   "err": err})


def get_registration_form(request):
    doctors = Doctor.objects.all()
    return render(request, template_name="registration/registration.html", context={"doctors": doctors})


def send_contract_num(request):
    contract_num = get_rand_contract_num()
    print(contract_num)
    ts_message = TurboSMSMessage(contract_num=contract_num, recipients=[request.POST["phone_number"]])
    ts_message.send()
    return HttpResponse(contract_num)


def validate_registration(request):
    try:
        user = User.objects.create_user(username=request.POST["phone_number"],
                                        password=request.POST["contract_num"],
                                        first_name=request.POST["name"],
                                        last_name=request.POST["lastname"])
        user.save()
        Patient().create_patient_from_dict(user, request.POST)
        return HttpResponseRedirect(redirect_to="/index")
    except IntegrityError:
        doctors = Doctor.objects.all()
        return render(request,
                      template_name="registration/registration.html",
                      context={"user_already_exists": True,
                               "doctors": doctors})


def get_full_time(tm: str) -> str:
    time_lst = tm.split()
    time = time_lst[0].split(":")
    if time_lst[1] == "a.m." and time[0] == "12":
        return "00:" + time[1]
    elif time_lst[1] == "a.m.":
        return time_lst[0]
    elif time_lst[1] == "p.m." and time[0] == "12":
        return "12:" + time[1]
    return str(int(time[0]) + 12) + ":" + time[1]


def get_appointments_dates(appointments) -> list[datetime.datetime]:
    app_dates = []
    for app in appointments:
        app_date = app.start_datetime
        if app_date.date() not in map(lambda dt_tm: dt_tm.date(), app_dates):
            app_dates.append(app_date)
    return list(map(lambda dt_tm: dt_tm.strftime("%d.%m.%Y"), app_dates))


class UserCabinet(ListView):
    model = Recording
    template_name = "clinic/pages/user-cabinet.html"
    context_object_name = "appointments"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = datetime.datetime.now()
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(person__user=self.request.user,
                                             schedule__start_datetime__gte=datetime.datetime.now() - datetime.timedelta(
                                                 days=5)).order_by("schedule__start_datetime")
