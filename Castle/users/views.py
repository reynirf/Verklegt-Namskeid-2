from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, "users/login.html")

def register(request):
    return render(request, "users/register.html")

def forgot_pass(request):
    return render(request, "users/forgot_pass.html")