from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from .models import User_info

class NewUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user has already registered an account with this email")
        return email

    name = forms.CharField(max_length=255, required=True)
    phone = forms.IntegerField(required=True)
    email = forms.CharField(max_length=100, required=True)
    seller = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'seller', 'password1', 'password2')

class Edit_buyer(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(Edit_buyer, self).__init__(*args, **kwargs)

        for fieldname in ['name', 'phone', 'email', 'password']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user has already registered an account with this email")
        return email

    class Meta:
        model = User_info
        fields = ('name', 'phone', 'email', 'password')

