from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "apartments/home.html")

def apartment_list(request):
    return render(request, "apartments/apartment_list.html")

def login(request):
    return render(request, "login_register.html")