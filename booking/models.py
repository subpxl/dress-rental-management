from inspect import CO_ASYNC_GENERATOR
from django.urls import reverse
from django.db import models
from catalouge.models import Product
from config.config import Config
from seller.models import Shop, Seller,Tax_and_Quantity
from shortuuid.django_fields import ShortUUIDField

STATUS = Config.STATUS

class Customer(models.Model):
    name = models.CharField(max_length=500)
    mobilenumber = models.CharField(max_length=500)
    whatsappNumber = models.CharField(max_length=500,null=True,blank=True)
    address = models.CharField(max_length=500)
    email=models.EmailField(null=True,blank=True)

    def __str__(self):
        return "%s " % (self.name)

    def get_absolute_url(self):
        return reverse("customer_list")

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    shop=models.ForeignKey(Shop,on_delete=models.PROTECT)
    orderdate = models.DateField(auto_now_add=True)
    startDate = models.DateField()
    startTime = models.CharField(max_length=15,choices=Config.DayTime)
    endTime = models.CharField(max_length=15,choices=Config.DayTime)
    endDate = models.DateField()
    totalAmount = models.PositiveIntegerField()
    amountPaid = models.PositiveIntegerField()
    amountDue = models.IntegerField()
    subtotal_price=models.PositiveIntegerField(null=True)
    subtotal_tax=models.PositiveIntegerField(null=True)
    discount = models.PositiveIntegerField(default=0,null=True)
    products = models.ManyToManyField(Product ,blank=False)
    orderNo = ShortUUIDField(length=6, max_length=21,  unique=True, db_index=True, editable=False)
    referenceNo = models.CharField(max_length=500, default="", null=True, blank=True)
    seller=models.ForeignKey(Seller,on_delete=models.PROTECT)
    note = models.CharField(max_length=500,blank=True,null=True)
    status = models.CharField(
        max_length=500, choices=STATUS,default=Config.Booked)
    final_paid = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s " % (self.shop)

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
    description = models.CharField(max_length=500)
    size = models.CharField(max_length=500)
    status = models.CharField(max_length=25)
    price = models.PositiveIntegerField()
    tax=models.ForeignKey(Tax_and_Quantity,on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s , %s" % (self.product,self.booking)
