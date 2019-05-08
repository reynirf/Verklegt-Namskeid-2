from django.urls import  path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("forgot_pass", views.forgot_pass, name="forgot_pass")
]