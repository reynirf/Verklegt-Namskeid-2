from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, "users/login_register.html")

def forgot_pass(request):
    return render(request, "users/forgot_pass.html")