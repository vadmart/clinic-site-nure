from django.db import models
from django import forms
from phonenumber_field.formfields import PhoneNumberField

SENDING_CHOICES = [
    ("telegram", ""),
    ("sms", "")
]


class ContractForm(forms.Form):
    template_name = "clinic/forms/contract_form.html"

    class StreetTypes(models.TextChoices):
        STREET = "вул", "Вулиця"
        AVENUE = "просп", "Проспект"
        BOULEVARD = "бул", "Бульвар"

    doctor_lfp = forms.CharField(label="Сімейний лікар", max_length=100)
    person_lastname = forms.CharField(label="Прізвище", max_length=30)
    person_name = forms.CharField(label="Ім'я", max_length=15)
    person_phone_number = PhoneNumberField(label="Номер телефону")
    street_type = forms.ChoiceField(label="Тип вулиці", choices=StreetTypes.choices)
    street_name = forms.CharField(label="Назва вулиці")
    house_number = forms.CharField(label="Номер вулиці")
    flat_no = forms.CharField(label="Номер квартири")
    post_index = forms.CharField(label="Поштовий індекс")
    telegram = forms.RadioSelect(choices=SENDING_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "textholder"

    def user_exists(self):
        self.person_phone_number.errors
