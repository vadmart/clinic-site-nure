from django.shortcuts import render


# Create your views here.
def index(request, doctor_img_name="default_photo"):
    return render(request, template_name="clinic/index.html", context={"lang": request.LANGUAGE_CODE,
                                                                       "doctor_img_name": doctor_img_name})


def get_schedule(request):
    return render(request, template_name="clinic/pages/schedule-work.html", context={"lang": request.LANGUAGE_CODE})


def get_contacts(request):
    return render(request, template_name="clinic/pages/contacts.html", context={"lang": request.LANGUAGE_CODE})


def get_vacancy(request):
    return render(request, template_name="clinic/pages/vacancy.html", context={"lang": request.LANGUAGE_CODE})


def quiz(request):
    return render(request, template_name="clinic/pages/", context={"lang": request.LANGUAGE_CODE})


def get_staff(request):
    return render(request, template_name="clinic/pages/staff.html", context={"lang": request.LANGUAGE_CODE})


def get_reviews(request):
    return render(request, template_name="clinic/pages/reviews.html", context={"lang": request.LANGUAGE_CODE})


def get_appointment_page(request):
    return render(request, template_name="clinic/pages/making-an-appointment.html", context={"lang": request.LANGUAGE_CODE})
