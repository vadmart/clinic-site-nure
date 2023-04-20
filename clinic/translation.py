from modeltranslation.translator import register, TranslationOptions
from .models import Doctor, DoctorCategory


@register(DoctorCategory)
class DoctorCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ("name", "lastname", "patronymic")
