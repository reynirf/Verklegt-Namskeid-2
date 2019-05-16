from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import requests

from apartments.models import Apartment
from .models import Buyer, User_info
from sellers.models import Seller


class NewUserForm(UserCreationForm):
    # A form for user registration
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        # Checking that the email entered is valid
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user has already registered an account with this email")
        return email

    name = forms.CharField(max_length=255, required=True)
    phone = forms.IntegerField(required=False)
    email = forms.CharField(max_length=100, required=True)
    seller = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'seller', 'password1', 'password2')

class Edit_buyer(UserChangeForm):
    # A form used when editing buyer profile
    password = None
    def __init__(self, *args, **kwargs):
        super(Edit_buyer, self).__init__(*args, **kwargs)
        for fieldname in ['name', 'phone']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User_info
        fields = ('name', 'phone')

class Edit_image(UserChangeForm):
    # A form for changing a buyer's profile image
    password = None
    def __init__(self, *args, **kwargs):
        super(Edit_image, self).__init__(*args, **kwargs)
        for fieldname in ['profile_pic']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = 'https://website.com/image.png'

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data['profile_pic']
        if not self.validateImage(profile_pic):
            raise ValidationError("Image is not valid / URL is broken")
        return profile_pic

    def validateImage(self, url):
        req = requests.head(url)
        return req.status_code == requests.codes.ok

    class Meta:
        model = Buyer
        fields = ('profile_pic',)

class Edit_logo(UserChangeForm):
    # A form for changing a seller's logo
    password = None
    def __init__(self, *args, **kwargs):
        super(Edit_logo, self).__init__(*args, **kwargs)
        for fieldname in ['logo']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = 'https://website.com/image.png'

    def clean_profile_pic(self):
        logo = self.cleaned_data['logo']
        if not self.validateImage(logo):
            raise ValidationError("Image is not valid / URL is broken")
        return logo

    def validateImage(self, url):
        req = requests.head(url)
        return req.status_code == requests.codes.ok

    class Meta:
        model = Seller
        fields = ('logo',)

class MultiWidgetBasic(forms.widgets.MultiWidget):
    # A widget used to process multiple entries when adding images for a new apartment
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'https://website.com/image.png',
            'autocomplete': 'off'
        }) for _ in range(20)]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(" ")
        else:
            return []


class MultiExampleField(forms.fields.MultiValueField):
    # A field used to add multiple images for a new apartment
    widget = MultiWidgetBasic

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=999, required=False)]
        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        return ",".join(values)


class Add_apartment(ModelForm):
    # A form used when adding a new apartment, makes use of MultiWidgetBasic
    # and MultiExampleField
    images = MultiExampleField(required=False)
    class Meta:
        room_choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6+'))
        model = Apartment
        exclude = ['id', 'sold', 'date_added', 'seller']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Þórláksgeisli 29',
                'autocomplete': 'off'
            }),
            'zip_code': forms.Select(attrs={
                'class':'form-control w-75',
                'autocomplete': 'off'
            }),
            'rooms': forms.Select(choices=room_choices, attrs={
                'class':'form-control w-50'
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control w-50',
                'type': 'number',
                'placeholder': '200',
                'min': '0',
                'max': '500',
                'autocomplete': 'off'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control w-50',
                'type': 'number',
                'placeholder': '45000000',
                'min': '0',
                'max': '200000000',
                'autocomplete': 'off'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '...',
                'autocomplete': 'off'
            }),
            'main_pic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'https://website.com/image.png',
                'autocomplete': 'off'
            })
        }


class Edit_seller(UserChangeForm):
    # A form for editing a seller's information
    password = None
    class Meta:
        model = Seller
        fields = ('description', 'address', 'zip_code')