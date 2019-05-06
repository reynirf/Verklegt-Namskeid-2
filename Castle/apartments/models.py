from django.db import models

class Apartment(models.Model):
    address = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    rooms = models.IntegerField()
    size = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=999)
    date_added = models.DateField()
