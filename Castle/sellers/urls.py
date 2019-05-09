from django.urls import  path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.sellers_list, name="sellers_list"),
    url(r'(?P<pk>\d+)/$', views.seller_info, name="seller_info")
]