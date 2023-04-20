from django.contrib import admin
from clinic.models import *
from modeltranslation.admin import TranslationAdmin


class DoctorCategoryAdmin(TranslationAdmin):
    fieldsets = [
        (u'DoctorCategory', {"fields": ("name",)})
    ]


class DoctorAdmin(TranslationAdmin):
    prepopulated_fields = {"slug": ("lastname", "name", "patronymic")}


# Register your models here.
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorCategory, DoctorCategoryAdmin)
admin.site.register(DoctorPhoneNumber)
admin.site.register(Patient)
admin.site.register(Review)
admin.site.register(Recording)
admin.site.register(Cabinet)
admin.site.register(Schedule)
