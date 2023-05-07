from django.contrib import admin
from clinic.models import *
from modeltranslation.admin import TranslationAdmin


class DoctorCategoryAdmin(TranslationAdmin):
    fieldsets = [
        (u'DoctorCategory', {"fields": ("name",)})
    ]
    list_display = ("id", "name")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "__str__", "created_at")


class DoctorAdmin(TranslationAdmin):
    prepopulated_fields = {"slug": ("lastname", "name", "patronymic")}
    list_display = ("full_name", "category", "work_start_date")


# Register your models here.
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorCategory, DoctorCategoryAdmin)
admin.site.register(DoctorPhoneNumber)
admin.site.register(Patient)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Recording)
admin.site.register(Cabinet)
admin.site.register(Schedule)
