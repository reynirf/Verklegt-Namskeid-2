from django.db import models
from users.models import User
from users.models import Buyer

class Seller(models.Model):
    description = models.CharField(max_length=999, null=True)
    address = models.CharField(max_length=255, null=True)
    zip_code = models.IntegerField(null=True)
    logo = models.CharField(max_length=999, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Sales(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    apartment = models.ForeignKey('apartments.Apartment', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.DO_NOTHING)
    date_sold = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
