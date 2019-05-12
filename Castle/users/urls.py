from django.contrib.auth.views import LoginView, LogoutView
from django.urls import  path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout", LogoutView.as_view(next_page='homepage'), name="logout"),
    path("forgot_pass", views.forgot_pass, name="forgot_pass"),
    path("register_success", views.register_success, name="register_success"),
    path("profile", views.profile, name="profile")
]