from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField

phone_validator = RegexValidator(r"\+38\d{10}", "Номер повинен починатися з +38 та складатися з 10 цифр")


class ContractForm(forms.Form):
    template_name = "clinic/forms/contract_form.html"

    class StreetTypes(models.TextChoices):
        STREET = "STR", _("Вулиця")
        AVENUE = "AVE", _("Проспект"),
        BOULEVARD = "BLV", _("Бульвар")

    doctor_fio = forms.CharField(label="Сімейний лікар", max_length=100)
    person_lastname = forms.CharField(label="Прізвище", max_length=30)
    person_name = forms.CharField(label="Ім'я", max_length=15)
    person_phone = PhoneNumberField(label="Номер телефону")
    street_type = forms.ChoiceField(label="Тип вулиці", choices=StreetTypes.choices)
    street_name = forms.CharField(label="Назва вулиці")
    street_no = forms.CharField(label="Номер вулиці")
    flat_no = forms.CharField(label="Номер квартири")
    post_index = forms.CharField(label="Поштовий індекс")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "textholder"
