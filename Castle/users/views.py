from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.

def login(request):
    return render(request, "users/login.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "users/register.html", {
        'form': UserCreationForm()
    })

def forgot_pass(request):
    return render(request, "users/forgot_pass.html")