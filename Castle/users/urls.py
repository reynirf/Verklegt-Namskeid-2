from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout", LogoutView.as_view(next_page='homepage'), name="logout"),
    path("forgot_pass", views.forgot_pass, name="forgot_pass"),
    path("register_success", views.register_success, name="register_success"),
    path("profile", views.profile, name="profile"),
    path("edit_user", views.edit_user, name="edit_user"),

    url(r'^password_reset/$', PasswordResetView.as_view(template_name='users/reset_password.html'), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='users/reset_password_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='users/reset_password_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'), name='password_reset_complete'),
]
