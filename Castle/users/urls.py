from django.urls import  path
from . import views

urlpatterns = [
    path("login_register", views.login, name="login_register"),
    path("forgot_pass", views.forgot_pass, name="forgot_pass")
]