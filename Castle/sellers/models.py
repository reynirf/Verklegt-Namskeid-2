from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    phone = models.IntegerField()
    email = models.CharField(max_length=100)

class Sales(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    apartment = models.ForeignKey('apartments.Apartment', on_delete=models.CASCADE)
    # buyer = models.ForeignKey(Buyer)
    date_sold = models.DateField()
    price = models.IntegerField()
