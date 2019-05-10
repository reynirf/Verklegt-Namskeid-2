from django.db import models
from django.contrib.auth.models import User
from django import forms

class User(models.Model):
    username = models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=16)
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

class NewUserForm(forms.ModelForm):
    username = forms.CharField(max_length=25)
    name = forms.CharField(max_length=255)
    phone = forms.IntegerField()
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=16)
    security_question = forms.CharField(max_length=255)
    security_answer = forms.CharField(max_length=255)
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'password', 'security_question', 'security_answer',)

class Buyer(models.Model):
    profile_pic = models.CharField(max_length=999, blank=True)
    credit_card = models.CharField(max_length=16, blank=True)
    cc_expires = models.CharField(max_length=5, blank=True)
    cc_cvc = models.IntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

