from django.shortcuts import render


# Create your views here.
def index(request, doctor_img_name="default_photo"):
    return render(request, template_name="clinic/index.html", context={"lang": request.LANGUAGE_CODE,
                                                                       "doctor_img_name": doctor_img_name})


def get_schedule(request):
    return render(request, template_name="clinic/pages/schedule-work.html", context={})


def get_contacts(request):
    return render(request, template_name="clinic/pages/contacts.html", context={})


def get_vacancy(request):
    return render(request, template_name="clinic/pages/vacancy.html", context={})


def quiz(request):
    return render(request, template_name="clinic/pages/")


def get_staff(request):
    return render(request, template_name="clinic/pages/staff.html")


def get_reviews(request):
    return render(request, template_name="clinic/pages/reviews.html")


def get_appointment_page(request):
    return render(request, template_name="clinic/pages/making-an-appointment.html")
