from django.db import models
from django.contrib.auth.models import User

class User_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    email = models.CharField(max_length=100)
    seller = models.BooleanField(default=False)
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

class Buyer(models.Model):
    profile_pic = models.CharField(max_length=999, null=True)
    credit_card = models.CharField(max_length=16, null=True)
    cc_expires = models.CharField(max_length=5, null=True)
    cc_cvc = models.IntegerField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

