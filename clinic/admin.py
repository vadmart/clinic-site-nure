from django.contrib import admin
from clinic.models import *

# Register your models here.
admin.site.register(DoctorCategories)
admin.site.register(Doctors)
admin.site.register(Cabinets)
admin.site.register(DoctorsCabinets)
admin.site.register(Persons)
admin.site.register(Reviews)
admin.site.register(Recordings)
admin.site.register(WeekDays)
admin.site.register(DoctorWorkingSchedule)
admin.site.register(PhoneNumbers)

