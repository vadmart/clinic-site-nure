from django.db import models
import textwrap
from django.utils import timezone


# Create your models here.

class DoctorCategories(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Doctors(models.Model):
    name = models.CharField(max_length=15)
    lastname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=20)
    category_id = models.ForeignKey(DoctorCategories, on_delete=models.SET_NULL, null=True)
    work_start_date = models.DateField()

    def __str__(self):
        return f"{self.lastname} {self.name} {self.patronymic}"


class Cabinets(models.Model):
    no = models.CharField(max_length=4)

    def __str__(self):
        return self.no


class DoctorsCabinets(models.Model):
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    cabinet_id = models.ForeignKey(Cabinets, on_delete=models.CASCADE)

    def __str__(self):
        return f"Doctor: {self.doctor_id.lastname} {self.doctor_id.name}, CabinetNo.: {self.cabinet_id.no}"


class Persons(models.Model):
    doctor_id = models.ForeignKey(to=Doctors, on_delete=models.CASCADE)
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


class Reviews(models.Model):
    doctor_id = models.ForeignKey(to=Doctors, on_delete=models.CASCADE)
    person_id = models.ForeignKey(to=Persons, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    datetime = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return textwrap.shorten(self.text, 30)


class Recordings(models.Model):
    person_id = models.ForeignKey(Persons, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    health_complaint = models.CharField(max_length=255)
    was_patient_present = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.person_id.name}, To: {self.doctor_id.name}"


class WeekDays(models.Model):
    name = models.CharField(max_length=9)

    def __str__(self):
        return self.name


class DoctorWorkingSchedule(models.Model):
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    week_day_id = models.ForeignKey(WeekDays, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Doctor: {self.doctor_id.lastname} {self.doctor_id.name}, week_day: {self.week_day_id.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["doctor_id", "week_day_id"], name="pk_doctor_working_schedule")
        ]


class PhoneNumbers(models.Model):
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    value = models.CharField(max_length=12)

    def __str__(self):
        return self.doctor_id.name
