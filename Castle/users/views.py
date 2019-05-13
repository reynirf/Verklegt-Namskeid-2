from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages


from sellers.models import Seller
from .models import User_info, Buyer, Search_history
from .forms import NewUserForm


import urllib
import json

from django.contrib.auth import authenticate

# Create your views here.

def register(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode('utf-8')
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            result = json.load(response)
            ''' End reCAPTCHA validation '''

            if result['success']:
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
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                print('test')
                #return redirect("register")
        print(form.errors)
    return render(request, "users/register.html", {
        'form': form
    })

@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        User_info.objects.create(user=instance)
    instance.user_info.save()

def forgot_pass(request):
    return render(request, "users/reset_password.html")

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
                   'buyer': Buyer.objects.filter(user=request.user.id).first(),
                   'history': Search_history.objects.filter(user=request.user.id).order_by('-search_date')[:12]}
        return render(request, "users/buyer_profile.html", context)