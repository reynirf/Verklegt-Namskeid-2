from django import forms

class ContactInfoForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    ssn = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}), required=True)
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    address = forms.CharField(max_length=255,  widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    zipcode = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}), required=True)
    city = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

class PaymentInfoForm(forms.Form):
    cardholder = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    cardnumber = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}), required=True)
    expires = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control w-25', 'type': 'number'}), required=True)
    cvc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control w-25', 'type': 'number'}), required=True)