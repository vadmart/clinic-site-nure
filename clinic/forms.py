from django.contrib.auth.views import LogoutView


class ClinicLogout(LogoutView):
    template_name = "clinic/index.html"
