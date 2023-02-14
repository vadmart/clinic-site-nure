from django.db import models
import textwrap
from django.utils import timezone
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
from bot.models import ContractInfo


# Create your models here.

class DoctorCategory(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=15)
    lastname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=20)
    category = models.ForeignKey(DoctorCategory, on_delete=models.SET_NULL, null=True)
    work_start_date = models.DateField()
    image_name = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.lastname} {self.name} {self.patronymic}"

    @staticmethod
    def get_doctors_by_input(input_value) -> QuerySet | list:
        return Doctor.objects.annotate(fullname=Concat("lastname", V(" "), "name", V(" "), "patronymic")). \
            filter(Q(fullname__icontains=input_value)).values_list("lastname", "name",
                                                                   "patronymic") \
            if input_value != "" else []


class Cabinet(models.Model):
    no = models.CharField(max_length=4)
    floor = models.IntegerField(default=0)

    def __str__(self):
        return self.no


class DoctorCabinet(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Doctor: {self.doctor.lastname} {self.doctor.name}, CabinetNo.: {self.cabinet.no}"


class Person(models.Model):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    lastname = models.CharField(max_length=30)
    contract_num = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    street_type = models.CharField(max_length=10)
    street_name = models.CharField(max_length=40)
    house_number = models.CharField(max_length=4)
    flat_number = models.CharField(max_length=4)
    post_index = models.IntegerField()

    def __str__(self):
        return f"{self.lastname} {self.name}"

    def add_info(self, contract: ContractInfo):
        self.doctor = Doctor.objects.get(lastname=contract.doctor_chat.lastname,
                                         name=contract.doctor_chat.name,
                                         patronymic=contract.doctor_chat.patronymic)
        self.name = contract.person_firstname
        self.lastname = contract.person_lastname
        self.contract_num = contract.contract_num
        self.phone_number = contract.person_number
        self.street_type = contract.street_type
        self.street_name = contract.street_name
        self.house_number = contract.house_number
        self.flat_number = contract.flat_number
        self.post_index = contract.post_index
        self.save(force_insert=True)


class Review(models.Model):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    datetime = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return textwrap.shorten(self.text, 30)


class Recording(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    health_complaint = models.CharField(max_length=255)
    was_patient_present = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.person.name}, To: {self.doctor.name}"


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    dt_tm = models.DateTimeField("date_time")
    is_busy = models.BooleanField(default=False)

    def __str__(self):
        return f"Doctor: {self.doctor.lastname} {self.doctor.name}, datetime: {self.dt_tm}"


class PhoneNumber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    value = models.CharField(max_length=12)

    def __str__(self):
        return self.doctor.name
