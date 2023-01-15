from django.db import models
import textwrap
from django.utils import timezone


# Create your models here.

class DoctorCategory(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=15)
    lastname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=20)
    category_id = models.ForeignKey(DoctorCategory, on_delete=models.SET_NULL, null=True)
    work_start_date = models.DateField()
    image_name = models.CharField(max_length=255, default="")

    def get_link(self):
        pass

    def __str__(self):
        return f"{self.lastname} {self.name} {self.patronymic}"


class Cabinet(models.Model):
    no = models.CharField(max_length=4)
    floor = models.IntegerField(default=0)

    def __str__(self):
        return self.no


class DoctorCabinet(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    cabinet_id = models.ForeignKey(Cabinet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Doctor: {self.doctor_id.lastname} {self.doctor_id.name}, CabinetNo.: {self.cabinet_id.no}"


class Person(models.Model):
    doctor_id = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    lastname = models.CharField(max_length=30)
    contract_num = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=12)
    street_type = models.CharField(max_length=10)
    street_name = models.CharField(max_length=40)
    house_number = models.CharField(max_length=4)
    flat_number = models.CharField(max_length=4)
    post_index = models.IntegerField()

    def __str__(self):
        return f"{self.lastname} {self.name}"


class Review(models.Model):
    doctor_id = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    person_id = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    datetime = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return textwrap.shorten(self.text, 30)


class Recording(models.Model):
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    health_complaint = models.CharField(max_length=255)
    was_patient_present = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.person_id.name}, To: {self.doctor_id.name}"


class Schedule(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    dt_tm = models.DateTimeField("date_time")
    is_busy = models.BooleanField(default=False)

    def __str__(self):
        return f"Doctor: {self.doctor_id.lastname} {self.doctor_id.name}, datetime: {self.dt_tm}"


class PhoneNumber(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    value = models.CharField(max_length=12)

    def __str__(self):
        return self.doctor_id.name
