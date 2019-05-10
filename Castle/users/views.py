from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import NewUserForm
from django.contrib.auth import authenticate

# Create your views here.

def login(request):
    print('hello')
    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print('lamfo')

        return render(request, 'users/forgot_pass.html')

    else:
        return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            print(form)
            print('lol')
            form.save()
            return redirect("login")
    return render(request, "users/register.html", {
        'form':UserCreationForm()
                  })

def forgot_pass(request):
    return render(request, "users/forgot_pass.html")

def register_success(request):
    return render(request, "user/register_success")