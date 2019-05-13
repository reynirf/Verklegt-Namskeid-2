from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    name = forms.CharField(max_length=255, required=True)
    phone = forms.IntegerField(required=True)
    email = forms.CharField(max_length=100, required=True)
    seller = forms.BooleanField(required=False)
    CHOICES = (('What was your childhood nickname? ', 'What was your childhood nickname?'), ('In what city did you meet your spouse/significant other?', 'In what city did you meet your spouse/significant other?'), ("What is your oldest sibling's middle name?", "What is your oldest sibling's middle name?"), ("In what city or town was your first job?", 'In what city or town was your first job?'), ("What is the name of your favorite childhood friend?", 'What is the name of your favorite childhood friend?')
               )
    security_question = forms.ChoiceField(choices=CHOICES)
    security_answer = forms.CharField(max_length=255, required=True)
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'seller', 'password1', 'password2', 'security_question', 'security_answer',)