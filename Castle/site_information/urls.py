from django.urls import path
from . import views

urlpatterns = [
    path('about_us', views.site_information, name='about_us')
]