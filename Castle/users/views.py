from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import User
from .forms import NewUserForm
from django.contrib.auth import authenticate

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            print('user created')
            user.refresh_from_db()
            user.user_info.email = form.cleaned_data.get('email')
            user.user_info.name = form.cleaned_data.get('name')
            user.user_info.phone = str(form.cleaned_data.get('phone'))
            user.user_info.security_question = form.cleaned_data.get('security_question')
            user.user_info.security_answer = form.cleaned_data.get('security_answer')
            user.save()
            print('user info saved')
            return redirect("login")
        print(form.errors)
    return render(request, "users/register.html", {
        'form': NewUserForm
                  })

def forgot_pass(request):
    return render(request, "users/forgot_pass.html")

def register_success(request):
    return render(request, "users/register_success.html")

@login_required
def profile(request):
    context = {'user': request.user, 'info': request.user.user_info}
    return render(request, "users/profile.html", context)