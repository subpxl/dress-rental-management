from django.db import models
from django.urls import reverse
from accounts.models import User
from config.config import Config

class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    mobileNumber= models.CharField(max_length=100)

    def __str__(self):
        return "%s " % (self.name)

    # def get_absolute_url(self):
    #     return reverse("shop_list")

class Branch(models.Model):
    main_shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    mobileNumber= models.CharField(max_length=100)

    def __str__(self):
        return "%s " % (self.name)
        
class Seller(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE) 
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,null=True)
    role = models.CharField(
        max_length=255, choices=Config.ROLE_CHOICES, default=Config.Staff, blank=True, null=True)
    # cover_photo = models.ImageField(
    #     upload_to='seller/cover_photo', blank=True, null=True, default='/default/seller-profile.jpg')
    # banner = models.ImageField(
    #     upload_to='seller/banner', blank=True, null=True, default='/default/seller-profile.jpg')
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=255, null=True)
    # license = models.ImageField(upload_to='seller/license')
    # rating = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # num_of_reviews = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    # is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner_name = models.CharField(max_length=50, null=True)
    # reg_no = models.CharField(max_length=50, null=True)
    gst = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    # lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    # long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    # policy = models.TextField(null=True)
    # about = models.TextField(null=True)


    def __str__(self) :
        return f'{self.name}'


class Subscription(models.Model):
    plans = (
        ('Gold','Gold'),
        ('Diamond','Diamond'),
        ('Platinum','Platinum'),
    )
    STATUS = (
        ('Success' , "Success"),
        ('Failure' , "Failure"),
        ('Pending' , "Pending"),)
    seller = models.OneToOneField(Seller,on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=10,choices=plans,default='Gold')
    order_number = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    amount = models.IntegerField()
    status = models.CharField(choices=STATUS,max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=36, null=False, blank=False)
    signature_id = models.CharField(max_length=128, null=False, blank=False)
