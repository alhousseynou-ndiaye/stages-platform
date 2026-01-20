from django.contrib.auth.views import LoginView, LogoutView

class LoginViewCustom(LoginView):
    template_name = "accounts/login.html"

class LogoutViewCustom(LogoutView):
    pass
