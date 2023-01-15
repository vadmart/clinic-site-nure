import datetime
import telebot
from telebot import formatting

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from clinic.models import Doctor, DoctorCabinet, PhoneNumber, Person, Schedule, Recording
from datetime import date

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
    revs = dctr.review_set.all()
    return render(request, template_name="clinic/pages/reviews.html", context={"doctor": dctr,
                                                                               "revs": revs})


def make_appointment(request):
    return render(request, template_name="clinic/pages/making-an-appointment.html", context={})


def quiz(request):
    return render(request, template_name="clinic/pages/quiz.html", context={})


@csrf_exempt
def doctor_info(request) -> JsonResponse:
    patient_data = request.POST.dict()
    try:
        person = Person.objects.get(lastname=patient_data["lastname"], name=patient_data["name"],
                                    contract_num=patient_data["contract_num"])
        doctor: Doctor = person.doctor_id
        schedule_for_doctor = Schedule.objects.filter(doctor_id=doctor.id)
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
    r = Recording(person_id=person,
                  doctor_id=doctor,
                  datetime=datetime.datetime.strptime(record_data["dt_tm"], "%Y-%m-%d %H:%M"),
                  health_complaint=record_data["complaint"])
    r.save()
    sch = Schedule.objects.get(doctor_id=r.doctor_id, dt_tm=r.datetime)
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
