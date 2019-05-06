from django.shortcuts import render
from apartments.models import Apartment

# Create your views here.

def home(request):
    return render(request, "apartments/home.html")

def apartment_list(request, context={'apartments': Apartment.objects.all()}):
    return render(request, "apartments/apartment_list.html", context)

