from django.urls import  path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.apartment_list, name="apartment_list"),
    url(r'(?P<pk>\d+)/$', views.apartment_info, name="apartment_info"),
]
