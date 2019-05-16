from django import forms

class ContactInfoForm(forms.Form):
    # Form for contact information when buying an apartment
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'John Doe'
    }), required=True)
    ssn = forms.IntegerField(max_value=99999999999999999999, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'number',
        'placeholder': '1212122020'
    }), required=True)
    country = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Iceland'
    }), required=True)
    address = forms.CharField(max_length=255,  widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Þórláksgeisli 29'
    }), required=True)
    zipcode = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'number',
        'placeholder': '113'
    }), required=True)
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Reykjavík'
    }), required=True)

class PaymentInfoForm(forms.Form):
    # Form for payment information when buying an apartment
    cardholder = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'John Doe'
    }), required=True)
    cardnumber = forms.IntegerField(max_value=9999999999999999, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'number',
        'placeholder': '1234123412341234'
    }), required=True)
    # Setting the options for months in expires
    months = (
        ('01', '01'), ('02', '02'),('03', '03'),('04', '04'),('05', '05'),('06', '06'),
        ('07', '07'),('08', '08'),('09', '09'),('10', '10'),('11', '11'),('12', '12')
    )
    expires_month = forms.ChoiceField(choices=months)
    # Setting the options for years in expires
    years = (
        ('2019', '2019'), ('2020', '2020'),('2021', '2021'),('2022', '2022'),
        ('2023', '2023'),('2024', '2024'),('2025', '2025'),('2026', '2026'),
        ('2027', '2027'),('2028', '2028'),('2029', '2020')
        )
    expires_year = forms.ChoiceField(choices=years)
    cvc = forms.IntegerField(max_value=9999, widget=forms.TextInput(attrs={
        'class': 'form-control w-25',
        'type': 'number',
        'placeholder': '123'}
    ), required=True)