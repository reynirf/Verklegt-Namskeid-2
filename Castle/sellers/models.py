from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    phone = models.IntegerField()
    email = models.CharField(max_length=100)

