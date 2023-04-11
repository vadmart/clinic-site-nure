# Create your models here.
from django.db import models
import textwrap
from django.contrib.auth.models import User
from django.http import QueryDict


class DoctorCategory(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія доктора"
        verbose_name_plural = "Категорії докторів"


class Doctor(models.Model):
    name = models.CharField(max_length=15)
    lastname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=20)
    category = models.ForeignKey(DoctorCategory, on_delete=models.SET_NULL, null=True)
    work_start_date = models.DateField()
    image_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.lastname} {self.name} {self.patronymic}"

    class Meta:
        verbose_name = "Доктор"
        verbose_name_plural = "Доктори"


class DoctorPhoneNumber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    phone_number_value = models.CharField(max_length=20)

    def __str__(self):
        return f"Doctor: {self.doctor.lastname} {self.doctor.name}, phone: {self.phone_number_value}"

    class Meta:
        verbose_name = "Телефонний номер доктора"
        verbose_name_plural = "Телефонні номери докторів"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(to=Doctor, on_delete=models.SET_NULL, null=True)
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

    class Meta:
        verbose_name = "Пацієнт"
        verbose_name_plural = "Пацієнти"

    def create_patient_from_dict(self, user: User, dct: QueryDict):
        self.user = user
        self.doctor = Doctor.objects.get(pk=int(dct["doctor_choice"]))
        self.name = dct["name"]
        self.lastname = dct["lastname"]
        self.patronymic = dct["patronymic"]
        self.contract_num = dct["contract_num"]
        self.phone_number = dct["phone_number"]
        self.street_type = dct["street_type"]
        self.street_name = dct["street_name"]
        self.house_number = dct["house_number"]
        self.flat_number = dct["flat_number"]
        self.post_index = dct["post_index"]
        self.save(force_insert=True)


class Review(models.Model):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    commentator_lastname = models.CharField(max_length=20)
    commentator_name = models.CharField(max_length=20)
    commentator_email = models.EmailField()
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return textwrap.shorten(self.text, 30)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"


class Recording(models.Model):
    person = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    health_complaint = models.CharField(max_length=255)
    was_patient_present = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.person.name}, To: {self.doctor.name}"

    class Meta:
        verbose_name = "Запис на прийом"
        verbose_name_plural = "Записи на прийом"


class Cabinet(models.Model):
    cabinet_no = models.IntegerField(primary_key=True)
    cabinet_name = models.CharField(max_length=128)
    cabinet_description = models.CharField(max_length=255)

    def __str__(self):
        return f"Cabinet name: {self.cabinet_name}"

    class Meta:
        verbose_name = "Кабінет"
        verbose_name_plural = "Кабінети"


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    cabinet = models.ForeignKey(Cabinet, null=True, on_delete=models.SET_NULL)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Doctor: {self.doctor.lastname} {self.doctor.name}, date: {self.start_datetime.date()}"

    class Meta:
        verbose_name = "Графік роботи"
        verbose_name_plural = "Графіки роботи"
