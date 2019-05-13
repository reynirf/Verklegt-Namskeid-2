from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from sellers.models import Seller
from .models import User_info, Buyer
from .forms import NewUserForm
from django.contrib.auth import authenticate

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            print(form)
            print('user created')
            user.refresh_from_db()
            user.user_info.email = form.cleaned_data.get('email')
            user.user_info.name = form.cleaned_data.get('name')
            user.user_info.phone = str(form.cleaned_data.get('phone'))
            user.user_info.seller = form.cleaned_data.get('seller')
            print(user.user_info.seller)
            user.user_info.security_question = form.cleaned_data.get('security_question')
            user.user_info.security_answer = form.cleaned_data.get('security_answer')
            user.save()
            if user.user_info.seller == True:
                Seller.objects.create(user=user)
            else:
                Buyer.objects.create(user=user)
            print('user info saved')
            return redirect("login")
        print(form.errors)
    return render(request, "users/register.html", {
        'form': NewUserForm
                  })

@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        User_info.objects.create(user=instance)
    instance.user_info.save()

def forgot_pass(request):
    return render(request, "users/forgot_pass.html")

def register_success(request):
    return render(request, "users/register_success.html")

@login_required
def profile(request):
    if request.user.user_info.seller == True:
        context = {'user': request.user,
                   'info': request.user.user_info,
                   'seller': Seller.objects.filter(user=request.user.id).first()}
        return render(request, "users/seller_profile.html", context)
    else:
        context = {'user': request.user,
                   'info': request.user.user_info,
                   'buyer': Buyer.objects.filter(user=request.user.id).first()}
        return render(request, "users/buyer_profile.html", context)