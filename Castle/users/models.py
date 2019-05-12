from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class User_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    email = models.CharField(max_length=100)
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

@receiver(post_save, sender=User)
def update_user_info(sender, instance, created, **kwargs):
    if created:
        User_info.objects.create(user=instance)
    instance.user_info.save()

class Buyer(models.Model):
    profile_pic = models.CharField(max_length=999, blank=True)
    credit_card = models.CharField(max_length=16, blank=True)
    cc_expires = models.CharField(max_length=5, blank=True)
    cc_cvc = models.IntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

