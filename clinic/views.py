import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.translation import gettext as _

from clinic import clinic_bot, verification
from clinic.clinic_bot import is_num_in_contracts_info
from clinic.models import Doctor, DoctorCabinet, PhoneNumber, Person, Schedule, Recording, Review
from bot.models import ContractInfo
from datetime import date
from .forms import ContractForm


# Create your views here.
def index(request):
    return render(request, template_name="clinic/index.html", context={})


def staff(request):
    doctors = Doctor.objects.all()
    doc_cabs = DoctorCabinet.objects.all()
    dates = [(date.today() - doctor.work_start_date).days // 365 for doctor in doctors]
    phones = PhoneNumber.objects.all()
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


def reviews(request, doctor_id):
    dctr = Doctor.objects.get(id=doctor_id)
    revs = dctr.review_set.all()[::-1]
    return render(request, template_name="clinic/pages/reviews.html", context={"doctor": dctr,
                                                                               "revs": revs})


def make_appointment(request):
    return render(request, template_name="clinic/pages/making-an-appointment.html", context={})


@csrf_exempt
def doctor_info(request) -> JsonResponse:
    patient_data = request.POST.dict()
    try:
        person = Person.objects.get(lastname=patient_data["lastname"], name=patient_data["name"],
                                    contract_num=patient_data["contract_num"])
        doctor: Doctor = person.doctor
        schedule_for_doctor = Schedule.objects.filter(doctor=doctor)
        print(schedule_for_doctor)
        schedule_dct = {}
        for obj in schedule_for_doctor:
            if not obj.is_busy:
                dt_tm = str(obj.dt_tm).split()
                dt_tm[1] = dt_tm[1][:5]
                try:
                    schedule_dct[dt_tm[0]].append(dt_tm[1])
                except KeyError:
                    schedule_dct[dt_tm[0]] = [dt_tm[1]]
        return JsonResponse(
            {
                "status": "success",
                "personId": person.id,
                "doctorId": doctor.id,
                "lastname": doctor.lastname,
                "name": doctor.name,
                "patronymic": doctor.patronymic,
                "workSchedule": schedule_dct
            })
    except Person.DoesNotExist:
        return JsonResponse({"status": "undefined"})


@csrf_protect
def record(request):
    record_data = request.POST
    person = Person.objects.get(id=record_data["person_id"])
    doctor = Doctor.objects.get(id=record_data["doctor_id"])
    print(record_data)
    rec = Recording(person=person,
                    doctor=doctor,
                    datetime=datetime.datetime.strptime(record_data["dt_tm"], "%Y-%m-%d %H:%M"),
                    health_complaint=record_data["complaint"])
    rec.save()
    sch = Schedule.objects.get(doctor=rec.doctor, dt_tm=rec.datetime)
    sch.is_busy = True
    sch.save()
    clinic_bot.send_msg_about_recording_to_doctor(person, doctor, rec)
    return HttpResponse("successful")


@csrf_exempt
def check_person(request):
    person_data = request.POST.dict()
    try:
        p = Person.objects.get(lastname=person_data["lastname"],
                               name=person_data["name"],
                               contract_num=person_data["contract_num"])
        if p.doctor.id == int(person_data["doctor_id"]):
            return JsonResponse({"status": "canLeaveReview"})
    except Person.DoesNotExist:
        pass
    return JsonResponse({"status": "undefined"})


@csrf_protect
def add_review(request, doctor_id):
    review_data = request.POST
    dctr = Doctor.objects.get(id=review_data["doctor_id"])
    prsn = Person.objects.get(lastname=review_data["lastname"], name=review_data["name"])
    r = Review(doctor=dctr, person=prsn, text=review_data["review-text"])
    r.save()
    return HttpResponseRedirect(f"/reviews/{doctor_id}")
        

@csrf_protect
def contract_page(request):
    form = ContractForm()
    print(request.headers["Accept-Language"])
    if request.method == "POST":
        form.data = request.POST
        form.is_bound = True
        if form.is_valid():
            if form.data["chosen"] == "telegram" \
                    and not ContractInfo.objects.filter(person_number=form.data["person_phone_number"]) \
                    and not is_num_in_contracts_info(form.data["person_phone_number"]):
                clinic_bot.send_msg_about_contract_to_doctor(form.data.dict())
                return HttpResponseRedirect("https://t.me/StepFristBot")
            elif ContractInfo.objects.filter(person_number=form.data["person_phone_number"]):
                form.add_error("person_phone_number", "Користувач з таким номером телефону вже зареєстрований")
            elif is_num_in_contracts_info(form.data["person_phone_number"]):
                form.add_error("person_phone_number",
                               "Користувач з таким номером телефону вже відправив інформацію для контракту")
    return render(request, "clinic/pages/making-a-contract.html", {"form": form})


# @csrf_protect
# def code_submitting(request):
#     otp_code, phone_number = request.POST["verification_code"], request.POST["person_phone_number"]
#     if verification.check_verification_code(phone_number, otp_code):
#         form_data = json.loads(request.POST["form_data"])
#         clinic_bot.send_msg_about_contract_to_doctor(form_data)
#         return HttpResponseRedirect("https://t.me/StepFristBot")
#     else:
#         return render(request,
#                       template_name="clinic/pages/number_submitting.html",
#                       context={"phone": request.POST["person_phone_number"],
#                                "form_data": request.POST["form_data"]})


@csrf_exempt
def doctor_lfp(request):
    search_data = request.body.decode(encoding="utf-8")
    searched_doctors = Doctor.get_doctors_by_input(search_data)
    searched_doctors = list(map(lambda tup: " ".join(tup), searched_doctors))
    return JsonResponse({"searchedDoctors": searched_doctors})
