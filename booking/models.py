from inspect import CO_ASYNC_GENERATOR
from django.urls import reverse
from django.db import models
from catalouge.models import Product
from config.config import Config
from seller.models import Shop, Seller, Branch
from shortuuid.django_fields import ShortUUIDField

STATUS = Config.STATUS

class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    whatsappNumber = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "%s " % (self.name)

    def get_absolute_url(self):
        return reverse("customer_list")

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    orderdate = models.DateField(auto_now_add=True)
    startDate = models.DateField()
    startTime = models.CharField(max_length=15,choices=Config.DayTime)
    endTime = models.CharField(max_length=15,choices=Config.DayTime)
    endDate = models.DateField()
    totalAmount = models.PositiveIntegerField()
    amountPaid = models.PositiveIntegerField()
    amountDue = models.IntegerField()
    discount = models.PositiveIntegerField(default=0)
    products = models.ManyToManyField(Product ,blank=False)
    orderNo = ShortUUIDField(length=6, max_length=6,  unique=True, db_index=True, editable=False)
    referenceNo = models.CharField(max_length=100, default="", null=True, blank=True)
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)
    note = models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(
        max_length=100, choices=STATUS,default=Config.Booked)

    def __str__(self):
        return "%s " % (self.branch)

    def get_absolute_url(self):
        return reverse("booking_list")

    def available_count(self):
        count = self.bookedproduct_set.filter(product__status=Config.Available).count()
        return count

    class Meta:
        permissions = [
            ("user_create_booking", "Can create bookings"),
            ("user_update_booking", "Can update bookings"),
            ("user_delete_booking", "Can delete bookings"),
            ("user_view_booking", "Can view bookings"),
        ]

class BookedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    def __str__(self):
        return "%s , %s" % (self.product,self.booking)
