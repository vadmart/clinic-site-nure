from django.contrib import admin
from clinic.models import *

# Register your models here.
admin.site.register(DoctorCategory)
admin.site.register(Doctor)
admin.site.register(Cabinet)
admin.site.register(DoctorCabinet)
admin.site.register(Person)
admin.site.register(Review)
admin.site.register(Recording)
admin.site.register(Schedule)
admin.site.register(PhoneNumber)

