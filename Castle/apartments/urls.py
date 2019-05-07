from django.urls import  path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path("", views.apartment_list, name="apartment_list"),
    url(r'(?P<pk>\d+)/$', views.single_apartment, name="single_apartment"),
]
