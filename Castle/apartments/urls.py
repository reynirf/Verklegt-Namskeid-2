from django.urls import  path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.apartment_list, name="apartment_list"),
    url(r'(?P<pk>\d+)/$', views.apartment_info, name="apartment_info"),
    url(r'(?P<pk>\d+)/contact_information', views.buy_contact, name='buy_contact'),
    url(r'(?P<pk>\d+)/payment_information', views.buy_payment, name='buy_payment'),
    url(r'(?P<pk>\d+)/review', views.buy_review, name='buy_review'),
    url(r'(?P<pk>\d+)/success', views.buy_success, name='buy_success'),
    url(r'(?P<pk>\d+)/remove', views.remove_apartment, name='remove_apartment')
]
