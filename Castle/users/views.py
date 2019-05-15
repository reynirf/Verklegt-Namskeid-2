from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

from django.forms import modelformset_factory
from sellers.models import Seller
from .models import User_info, Buyer, Search_history
from .forms import NewUserForm


import urllib
import json
import ssl

from .models import User_info, Buyer
from .forms import NewUserForm, Edit_buyer, Edit_image, Edit_seller, Edit_logo
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
            sslcontext = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=sslcontext)
            result = json.load(response)
            ''' End reCAPTCHA validation '''

            if result['success']:
                user = form.save()
                user.refresh_from_db()
                user.user_info.email = form.cleaned_data.get('email')
                user.user_info.name = form.cleaned_data.get('name')
                user.user_info.phone = str(form.cleaned_data.get('phone'))
                user.user_info.seller = form.cleaned_data.get('seller')
                user.save()
                if user.user_info.seller == True:
                    Seller.objects.create(user=user)
                else:
                    Buyer.objects.create(user=user)
                return redirect("login")
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        print(form.errors)
    return render(request, "users/register.html", {
        'form': form
    })

@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    print('instance:', instance)
    print('created:', created)
    if created:
        User_info.objects.create(user=instance)
    instance.user_info.save()

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
                   'history': Search_history.objects.filter(user=request.user.id).order_by('-search_date')}
        return render(request, "users/buyer_profile.html", context)

@login_required
def edit_user(request):
    if request.user.user_info.seller:
        form = Edit_buyer(instance=request.user.user_info)
        form2 = Edit_seller(instance=request.user.seller)
        if request.method == "POST":
            form = Edit_buyer(request.POST, instance=request.user.user_info)
            form2 = Edit_seller(request.POST, instance=request.user.seller)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                return redirect('/users/profile')
    else:
        form = Edit_buyer(instance=request.user.user_info)
        if request.method == "POST":
            form = Edit_buyer(request.POST, instance=request.user.user_info)
            if form.is_valid():
                form.save()
                return redirect('/users/profile')
    if request.user.user_info.seller:
        args = {'form': form, 'form2': form2}
    else:
        args = {'form': form}
    return render(request, "users/edit_user.html", args)

@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/users/profile')
    args = {'form': form}
    return render(request, 'users/change_password.html', args)

@login_required
def change_image(request):
    if request.user.user_info.seller:
        form = Edit_logo(instance=request.user.seller)
        if request.method == "POST":
            form = Edit_logo(data=request.POST, instance=request.user.seller)
            if form.is_valid():
                form.save()
                return redirect('/users/profile')
        args = {'form': form}
        return render(request, 'users/change_image.html', args)
    else:
        form = Edit_image(instance=request.user.buyer)
        if request.method == "POST":
            form = Edit_image(data=request.POST, instance=request.user.buyer)
            if form.is_valid():
                form.save()
                #update_session_auth_hash(request, form.user)
                return redirect('/users/profile')
        args = {'form': form}
        return render(request, 'users/change_image.html', args)

#SELLER_REQUIRED?
@login_required
def add_apartment(request):
    if request.user.user_info.seller:
        form = add_apartment()
        if request.method == 'POST':
            apartment = add_apartment(data=request.POST)
            if form.is_valid():
                apartment.save()
        else:
            return render(request, "users/add_apartment.html", {
                'form': form
            })
    else:
        return redirect('homepage')
