from django import forms

class ContactInfoForm(forms.Form):
    name = forms.CharField(max_length=255)
    ssn = forms.IntegerField()
    country = forms.CharField()
    address = forms.CharField(max_length=255)
    zipcode = forms.IntegerField()
    city = forms.CharField()

