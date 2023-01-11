from django.shortcuts import render
from django.shortcuts import render
from clinic.models import Doctors, DoctorsCabinets, PhoneNumbers
from datetime import date


# Create your views here.
def index(request):
    return render(request, template_name="clinic/index.html", context={})


def staff(request):
    doctors = Doctors.objects.all()
    doc_cabs = DoctorsCabinets.objects.all()
    dates = [(date.today() - doctor.work_start_date).days // 365 for doctor in doctors]
    phones = PhoneNumbers.objects.all()
    return render(request, template_name="clinic/pages/staff.html", context={"doctors": doctors,
                                                                             "doc_cabs": doc_cabs,
                                                                             "phones": phones,
                                                                             "dates": dates})


def schedule(request):
    return render(request, template_name="clinic/pages/schedule-work.html", context={})


def contacts(request):
    return render(request, template_name="clinic/pages/contacts.html", context={})


def vacancy(request):
    return render(request, template_name="clinic/pages/vacancy.html", context={})


def reviews(request):
    return render(request, template_name="clinic/pages/reviews.html", context={})


def make_appointment(request):
    return render(request, template_name="clinic/pages/making-an-appointment.html", context={})


def quiz(request):
    return render(request, template_name="clinic/pages/quiz.html", context={})
