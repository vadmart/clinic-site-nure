from django.contrib import admin
from clinic.models import *
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _


class DoctorCategoryAdmin(TranslationAdmin):
    fieldsets = [
        (u'DoctorCategory', {"fields": ("name",)})
    ]
    list_display = ("id", "name")

    def name(self, obj):
        return obj.name

    name.short_description = _("Ім'я")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "__str__", "created_at")


class DoctorFilter(admin.SimpleListFilter):
    title = "Work start date"
    parameter_name = "work_start_date"

    def lookups(self, request, model_admin):
        res = []
        qs = Doctor.objects.order_by("-work_start_date__year").values_list("work_start_date__year").distinct()
        print(qs)
        for d in qs:
            res.append((d[0], d[0]))
        return res

    def queryset(self, request, queryset):
        return queryset.filter(work_start_date__year=self.value()) if self.value() else queryset


class DoctorAdmin(TranslationAdmin):
    prepopulated_fields = {"slug": ("lastname", "name", "patronymic")}
    list_display = ("full_name", "category", "work_start_date")
    list_filter = (DoctorFilter,)


class DoctorPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_numbers")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    @staticmethod
    def full_name(obj):
        return f"{obj.doctor.lastname} {obj.doctor.name} {obj.doctor.patronymic}"

    @staticmethod
    def phone_numbers(obj):
        txt = ""
        qs = DoctorPhoneNumber.objects.filter(doctor=obj.doctor)
        for i in range(len(qs)):
            txt += qs[i].phone_number_value
            if i != len(qs) - 1:
                txt += ", "
        return txt


class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "doctor_full_name")

    @staticmethod
    def full_name(obj):
        return f"{obj.lastname} {obj.name} {obj.patronymic}"

    @staticmethod
    def doctor_full_name(obj):
        return f"{obj.doctor.lastname} {obj.doctor.name} {obj.doctor.patronymic}"


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("full_name", "start_datetime", "end_datetime", "cabinet", "recording")

    @staticmethod
    def full_name(obj):
        return f"{obj.doctor.lastname} {obj.doctor.name} {obj.doctor.patronymic}"


class CabinetAdmin(admin.ModelAdmin):
    list_display = ("cabinet_no", "cabinet_name", "cabinet_short_description")

    @staticmethod
    def cabinet_short_description(obj):
        return textwrap.shorten(obj.cabinet_description, 50)


# Register your models here.
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorCategory, DoctorCategoryAdmin)
admin.site.register(DoctorPhoneNumber, DoctorPhoneNumberAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Recording)
admin.site.register(Cabinet, CabinetAdmin)
admin.site.register(Schedule, ScheduleAdmin)
