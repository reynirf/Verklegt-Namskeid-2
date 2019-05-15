from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from apartments.models import Zipcode, Apartment
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

class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={'class': 'form-control', 'placeholder':'https://website.com/image.png'}) for _ in range(20)]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(" ")
        else:
            return []


class MultiExampleField(forms.fields.MultiValueField):
    widget = MultiWidgetBasic

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=999, required=False)]
        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        return values.join(" ")


class Add_apartment(forms.Form):
    address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Þórláksgeisli 29'}))
    zip_code = forms.ModelChoiceField(queryset=Zipcode.objects.all(), widget=forms.Select(attrs={'class':'form-control w-75'}))
    room_choices = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6+','6+'))
    rooms = forms.ChoiceField(choices=room_choices, widget=forms.Select(attrs={'class':'form-control w-50'}))
    size = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control w-50', 'type': 'number', 'placeholder': '200'}))
    price = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control w-50', 'type': 'number', 'placeholder': '45000000'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}))
    main_pic = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'https://website.com/image.png'}))
    images = MultiExampleField(required=False)

    # class Meta:
    #     model = Apartment
    #     exclude = ['id', 'seller', 'sold', 'date_added']


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