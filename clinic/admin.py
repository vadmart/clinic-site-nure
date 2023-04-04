from django.contrib import admin
from clinic.models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(DoctorCategory)
admin.site.register(DoctorPhoneNumber)
admin.site.register(Patient)
admin.site.register(Review)
admin.site.register(Recording)
admin.site.register(Cabinet)
admin.site.register(Schedule)
