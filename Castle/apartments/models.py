from django.db import models
from sellers.models import Seller

class Zipcode(models.Model):
    town = models.CharField(max_length=30)

    def natural_key(self):
        return [self.town, self.id]

class Apartment(models.Model):
    address = models.CharField(max_length=255)
    zip_code = models.ForeignKey(Zipcode, on_delete=models.DO_NOTHING)
    rooms = models.IntegerField()
    size = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=999)
    main_pic = models.CharField(max_length=999)
    date_added = models.DateField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def natural_key(self):
        return [self.zip_code.natural_key()]

class Apartment_images(models.Model):
    image = models.CharField(max_length=999)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

class Apartment_featured(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
