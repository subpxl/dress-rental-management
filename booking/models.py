from inspect import CO_ASYNC_GENERATOR
from django.urls import reverse
from django.db import models
from catalouge.models import Product
from config.config import Config
# from seller.models import Shop
from seller.models import Seller
from shortuuid.django_fields import ShortUUIDField

STATUS = Config.STATUS

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    alternatenumber = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "%s " % (self.name)

    def get_absolute_url(self):
        return reverse("customer_list")

class Booking(models.Model):
    customerName = models.CharField(max_length=100)
    mobileNumber = models.CharField(max_length=100)
    alternateNumber = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    orderdate = models.DateField(auto_now_add=True)
    startDate = models.DateField()
    endDate = models.DateField()
    totalAmount = models.PositiveIntegerField()
    amountPaid = models.PositiveIntegerField()
    amountDue = models.PositiveIntegerField()
    products = models.ManyToManyField(Product ,blank=False, )
    orderNo = ShortUUIDField(length=6, max_length=6,  unique=True, db_index=True, editable=False)
    referenceNo = models.CharField(max_length=100, default="", null=True, blank=True)
    Seller=models.ForeignKey(Seller,on_delete=models.CASCADE,default=1)
    note = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(
        max_length=100, choices=STATUS,default=Config.Booked)

    def __str__(self):
        return "%s " % (self.customerName)

    def get_absolute_url(self):
        return reverse("booking_list")

    def available_count(self):
        count = self.bookedproduct_set.filter(product__status=Config.Available).count()
        return count


class BookedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    def __str__(self):
        return "%s , %s" % (self.product,self.booking)
