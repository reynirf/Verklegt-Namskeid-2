from django import forms

class ContactInfoForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    ssn = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}), required=True)
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    address = forms.CharField(max_length=255,  widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    zipcode = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}), required=True)
    city = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

