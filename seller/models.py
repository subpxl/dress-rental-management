from django.db import models
from django.urls import reverse

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    mobileNumber= models.CharField(max_length=100)

    def __str__(self):
        return "%s " % (self.name)

    def get_absolute_url(self):
        return reverse("shop_list")