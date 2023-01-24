from django.contrib import admin
from quiz.models import *

# Register your models here.
admin.site.register(InputType)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionAnswer)

