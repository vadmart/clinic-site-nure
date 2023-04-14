from django.shortcuts import render
from clinic.models import Doctor, Patient, Review, Recording
from django.http import HttpResponse, HttpResponseRedirect
from clinic.contract import get_rand_contract_num
from clinic.turbosms import TurboSMSMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.utils.translation import get_language
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
    return render(request, template_name="clinic/pages/")


def get_staff(request):
    doctors = Doctor.objects.all()
    return render(request, template_name="clinic/pages/staff.html", context={"doctors": doctors})


def get_reviews(request, doctor_ln):
    doctor = Doctor.objects.get(image_name=doctor_ln)
    return render(request, template_name="clinic/pages/reviews.html", context={"doctor": doctor})


def get_appointment_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="login")
    doctor = Patient.objects.get(user=request.user).doctor
    appointments = doctor.schedule_set.all()
    app_dates = []
    for app in appointments:
        app_date = app.start_datetime.strftime("%d.%m.%Y")
        if app_date not in app_dates:
            app_dates.append(app_date)
    print(appointments)
    return render(request, template_name="clinic/pages/making-an-appointment.html", context={"doctor": doctor,
                                                                                             "appointments": appointments,
                                                                                             "app_dates": app_dates})


def make_record(request):
    print(request.POST)
    return HttpResponseRedirect(redirect_to="index")


def get_registration_form(request):
    doctors = Doctor.objects.all()
    return render(request, template_name="registration/registration.html", context={"doctors": doctors})


def send_contract_num(request):
    contract_num = get_rand_contract_num()
    print(contract_num)
    ts_message = TurboSMSMessage(contract_num=contract_num, recipients=[json.loads(request.body)["phone_number"]])
    ts_message.send()
    return HttpResponse(contract_num)


def validate_registration(request):
    user = User.objects.create_user(username=request.POST["name"],
                                    last_name=request.POST["lastname"],
                                    password=request.POST["contract_num"])
    user.save()
    Patient().create_patient_from_dict(user, request.POST)
    return HttpResponseRedirect(redirect_to="/index")


def send_review(request):
    doctor = Doctor.objects.get(image_name=request.POST['doctor_lastname_name'])
    Review.objects.create(doctor=doctor,
                          patient=request.user.patient,
                          text=request.POST["review_text"])
    return HttpResponseRedirect(redirect_to=f"/reviews/{request.POST['doctor_lastname_name']}")


class ClinicLogin(LoginView):
    def get_success_url(self):
        return "index"


class ClinicLogout(LogoutView):
    template_name = "clinic/index.html"

    def get_success_url(self):
        return "index"
