from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    phone = forms.IntegerField()
    email = forms.CharField(max_length=100)
    seller = forms.BooleanField(required=False)
    security_question = forms.CharField(max_length=255)
    security_answer = forms.CharField(max_length=255)
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'seller', 'password1', 'password2')
