from django.shortcuts import render
from clinic.models import Doctor, Patient
from django.http import HttpResponse, HttpResponseRedirect
from clinic.contract import get_rand_contract_num
from clinic.turbosms import TurboSMSMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
    return render(request, template_name="clinic/pages/making-an-appointment.html")


def get_registration_form(request):
    doctors = Doctor.objects.all()
    return render(request, template_name="registration/registration.html", context={"doctors": doctors})


def send_contract_num(request):
    contract_num = get_rand_contract_num()
    print(contract_num)
    ts_message = TurboSMSMessage(contract_num=contract_num, recipients=[json.loads(request.body)["phone_number"]])
    # ts_message.send()
    return HttpResponse(contract_num)


def validate_registration(request):
    user = User.objects.create_user(username=request.POST["name"],
                                    last_name=request.POST["lastname"],
                                    password=request.POST["contract_num"])
    user.save()
    Patient().create_patient_from_dict(user, request.POST)
    return HttpResponseRedirect(redirect_to="/index")


def validate_login(request):
    auth_user = authenticate(request)
    return render(request, template_name="clinic/index.html")

