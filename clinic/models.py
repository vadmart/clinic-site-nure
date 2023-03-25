# Create your models here.
from django.db import models
import textwrap
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django.db.models.query import QuerySet


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
    image_name = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.lastname} {self.name} {self.patronymic}"


class Patient(models.Model):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    lastname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    contract_num = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    street_type = models.CharField(max_length=10)
    street_name = models.CharField(max_length=40)
    house_number = models.CharField(max_length=4)
    flat_number = models.CharField(max_length=4)
    post_index = models.IntegerField()

    def __str__(self):
        return f"{self.lastname} {self.name}"


class Review(models.Model):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    commentator_lastname = models.CharField(max_length=20)
    commentator_name = models.CharField(max_length=20)
    commentator_email = models.EmailField()
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return textwrap.shorten(self.text, 30)


class Recording(models.Model):
    person = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    health_complaint = models.CharField(max_length=255)
    was_patient_present = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.person.name}, To: {self.doctor.name}"


class WorkingTime(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    dt_tm = models.DateTimeField("date_time")
    is_busy = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Doctor: {self.doctor.lastname} {self.doctor.name}, datetime: {self.dt_tm}"


class Doctor_PhoneNumber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    value = models.CharField(max_length=12)

    def __str__(self):
        return self.doctor.name
