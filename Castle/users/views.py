from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from apartments.models import Apartment_images
from sellers.models import Seller
from .models import Search_history
from apartments.models import Apartment
from .models import User_info, Buyer
from .forms import NewUserForm, Edit_buyer, Edit_image, Edit_seller, Edit_logo, Add_apartment

import urllib
import json
import ssl


def register(request):
    # redirecting if user is already logged in
    if request.user.is_authenticated:
        return redirect('profile')
    form = NewUserForm()
    # POST method when the form has been submitted:
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            # Begin reCAPTCHA validation
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
            # End reCAPTCHA validation

            # If CAPTCHA is ok save information to user and user_info tables:
            if result['success']:
                user = form.save()
                user.refresh_from_db()
                user.user_info.email = form.cleaned_data.get('email')
                user.user_info.name = form.cleaned_data.get('name')
                user.user_info.phone = str(form.cleaned_data.get('phone'))
                user.user_info.seller = form.cleaned_data.get('seller')
                user.save()
                # Separating buyers and seller and saving to database:
                if user.user_info.seller == True:
                    Seller.objects.create(user=user)
                else:
                    Buyer.objects.create(user=user)
                return redirect("login")
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    # GET method when first loading the page:
    return render(request, "users/register.html", {
        'form': form
    })

@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    # Automatically saving user_info when user is created
    if created:
        User_info.objects.create(user=instance)
    instance.user_info.save()

@login_required
def profile(request):
    # Profile for sellers:
    if request.user.user_info.seller == True:
        # Getting all apartments for the seller
        all = Apartment.objects.filter(seller=request.user.seller.id)
        for_sale = all.filter(sold=False)
        sold = all.filter(sold=True)
        # Calculating the total price of sold apartments
        price = sold.aggregate(Sum('price'))['price__sum']
        context = {'user': request.user,
                   'info': request.user.user_info,
                   'seller': Seller.objects.filter(user=request.user.id).first(),
                   'apartments': all,
                   'sold_apartments': sold,
                   'for_sale': for_sale,
                   'money': price
                   }
        return render(request, "users/seller_profile.html", context)
    # Profile for buyers:
    else:
        context = {'user': request.user,
                   'info': request.user.user_info,
                   'buyer': Buyer.objects.filter(user=request.user.id).first(),
                   'history': Search_history.objects.filter(
                       user=request.user.id).order_by('-search_date')
                   }
        return render(request, "users/buyer_profile.html", context)

@login_required
def edit_user(request):
    # Editing a sellers profile
    if request.user.user_info.seller:
        # Two forms needed for user_info and seller tables
        form = Edit_buyer(instance=request.user.user_info)
        form2 = Edit_seller(instance=request.user.seller)
        if request.method == "POST":
            form = Edit_buyer(request.POST, instance=request.user.user_info)
            form2 = Edit_seller(request.POST, instance=request.user.seller)
            if form.is_valid() and form2.is_valid():
                # If they are valid, save and redirect to profile
                form.save()
                form2.save()
                return redirect('/users/profile')
    # Editing a buyers profile
    else:
        form = Edit_buyer(instance=request.user.user_info)
        if request.method == "POST":
            form = Edit_buyer(request.POST, instance=request.user.user_info)
            if form.is_valid():
                form.save()
                return redirect('/users/profile')
    # Sending the forms to the html template
    if request.user.user_info.seller:
        args = {'form': form, 'form2': form2}
    else:
        args = {'form': form}
    return render(request, "users/edit_user.html", args)

@login_required
def change_password(request):
    # Changing the password for a user
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            # updating the session with the logged in user
            update_session_auth_hash(request, form.user)
            return redirect('/users/profile')
    args = {'form': form}
    return render(request, 'users/change_password.html', args)

@login_required
def change_image(request):
    # Changing the logo for sellers:
    if request.user.user_info.seller:
        form = Edit_logo(instance=request.user.seller)
        if request.method == "POST":
            form = Edit_logo(data=request.POST, instance=request.user.seller)
            if form.is_valid():
                form.save()
                return redirect('/users/profile')
        args = {'form': form}
        return render(request, 'users/change_image.html', args)
    # Changing the profile picture for buyers:
    else:
        form = Edit_image(instance=request.user.buyer)
        if request.method == "POST":
            form = Edit_image(data=request.POST, instance=request.user.buyer)
            if form.is_valid():
                form.save()
                return redirect('/users/profile')
        args = {'form': form}
        return render(request, 'users/change_image.html', args)

@login_required
def add_apartment(request):
    # Adding a new apartment, only available if user is a seller
    if request.user.user_info.seller:
        form = Add_apartment()
        if request.method == 'POST':
            form = Add_apartment(data=request.POST)
            if form.is_valid():
                # Not committing as apartment has no seller
                apartment = form.save(commit=False)
                # Adding the seller and then saving
                apartment.seller = request.user.seller
                apartment.save()
                # Looping through the extra images and saving to database
                # if the value returned is not None
                for num in range(20):
                    num_str = 'images_' + str(num)
                    print(request.POST[num_str])
                    if request.POST[num_str] != "":
                        image = Apartment_images(
                            apartment=apartment,
                            image=request.POST[num_str]
                        )
                        image.save()
                return redirect('profile')
            else:
                return render(request, "users/add_apartment.html", {
                    'form': form
                })
        # Sending the form to the html template
        else:
            return render(request, "users/add_apartment.html", {
                'form': form
            })
    # Redirecting unauthorized user back to the homepage
    else:
        return redirect('homepage')
