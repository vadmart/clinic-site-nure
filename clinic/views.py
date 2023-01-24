import datetime
import telebot
from telebot import formatting

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q

from clinic.models import Doctor, DoctorCabinet, PhoneNumber, Person, Schedule, Recording, Review
from datetime import date
from .forms import ContractForm

API_TOKEN = "5107287131:AAF2wqmilqpXxmF9rf4mBL1oKC3U5Z35-hY"
bot = telebot.TeleBot(API_TOKEN)


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
    r = Recording(person=person,
                  doctor=doctor,
                  datetime=datetime.datetime.strptime(record_data["dt_tm"], "%Y-%m-%d %H:%M"),
                  health_complaint=record_data["complaint"])
    r.save()
    sch = Schedule.objects.get(doctor=r.doctor, dt_tm=r.datetime)
    sch.is_busy = True
    sch.save()
    bot.send_message(-1001728749709,
                     formatting.format_text(f"Особа " + formatting.hitalic(f"{person.lastname} {person.name}") +
                                            " записана на прийом до лікаря " +
                                            formatting.hitalic(
                                                f"{doctor.lastname} {doctor.name} {doctor.patronymic}.\n") +
                                            f"Дата: {r.datetime.date().strftime('%d.%m.%Y')}, час: {r.datetime.time().strftime('%H:%M')}\n" +
                                            "Скарга на здоров'я:", formatting.hitalic(
                         f'"{r.health_complaint}"')), parse_mode="HTML")

    return HttpResponse("successful")


@csrf_exempt
def check_person(request):
    person_data = request.POST.dict()
    try:
        p = Person.objects.get(lastname=person_data["lastname"],
                               name=person_data["name"],
                               contract_num=person_data["contract_num"])
        attendances = Recording.objects.filter(person_id=p.id, doctor_id=person_data["doctor_id"])
        for att in attendances:
            if att.was_patient_present:
                return JsonResponse({"status": "canLeaveReview"})
        return JsonResponse({"status": "didntVisitADoctor"})
    except Person.DoesNotExist:
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
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/")
    form = ContractForm()
    return render(request, "clinic/pages/making-a-contract.html", {"form": form})


@csrf_exempt
def doctor_fio(request):
    search_data = request.body.decode(encoding="utf-8")
    searched_doctors = Doctor.objects.filter(Q(lastname__icontains=search_data) |
                                             Q(name__icontains=search_data) |
                                             Q(patronymic__icontains=search_data)).values_list("lastname", "name",
                                                                                               "patronymic")
    searched_doctors = list(map(lambda tup: " ".join(tup), searched_doctors))
    return JsonResponse({"searchedDoctors": searched_doctors})
