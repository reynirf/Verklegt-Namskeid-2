from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Buyer, User_info
from sellers.models import Seller
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import requests


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
    phone = forms.IntegerField(required=False)
    email = forms.CharField(max_length=100, required=True)
    seller = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'seller', 'password1', 'password2')

class Edit_buyer(UserChangeForm):
    password = None
    def __init__(self, *args, **kwargs):
        super(Edit_buyer, self).__init__(*args, **kwargs)
        for fieldname in ['name', 'phone']:
            self.fields[fieldname].help_text = None

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     print(User.objects.filter(email=email).exists())
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("A user has already registered an account with this email")
    #     if not self.validateEmail(email):
    #         raise ValidationError("Email is not valid")
    #     return email
    #
    # def validateEmail(self, email):
    #     try:
    #         validate_email(email)
    #         return True
    #     except ValidationError:
    #         return False

    class Meta:
        model = User_info
        fields = ('name', 'phone')

class Edit_image(UserChangeForm):
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

class add_apartment(forms.Form):
    address = forms.CharField(max_length=255, required=True)
    zip_code = forms.Select()
    rooms = forms.Select()
    size = forms.IntegerField(required=True)
    price = forms.IntegerField(required=True)
    description = forms.CharField(required=True)
    main_pic = forms.CharField(required=True)


class Edit_seller(UserChangeForm):
    password = None
    #def __init__(self, *args, **kwargs):
    #    super(Edit_buyer, self).__init__(*args, **kwargs)
    #    for fieldname in ['description', 'address', 'zip_code']:
    #        self.fields[fieldname].help_text = None


    #def clean_email(self):
    #    email = self.cleaned_data['email']
    #    if User.objects.filter(email=email).exists():
    #        raise ValidationError("A user has already registered an account with this email")
    #    if not self.validateEmail(email):
    #        raise ValidationError("Email is not valid")
    #    return email

    #def validateEmail(self, email):
    #    try:
    #        validate_email(email)
    #        return True
    #    except ValidationError:
    #        return False

    class Meta:
        model = Seller
        fields = ('description', 'address', 'zip_code')