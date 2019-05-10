from django import forms

class NewUserForm(forms.Form):
    username = forms.CharField(max_length=25)
    name = forms.CharField(max_length=255)
    phone = forms.IntegerField()
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=16)
    security_question = forms.CharField(max_length=255)
    security_answer = forms.CharField(max_length=255)