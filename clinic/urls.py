from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pages/staff", views.staff, name="staff")
]
