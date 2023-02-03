from django.urls import reverse
from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    alternatenumber = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "%s " % (self.name)

    def get_absolute_url(self):
        return reverse("customer_list")
