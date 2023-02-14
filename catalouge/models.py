from django.db import models
from django.urls import reverse
from config.config import Config
from seller.models import Shop, Seller, Branch

class Category(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)

    def __str__(self):
        return "%s " % (self.name)

    def get_absolute_url(self):
        return reverse("category_list")
    
    def get_prod_count(self):
        return self.product_set.all().count()


class Product(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100,unique=True)
    color = models.CharField(max_length=100,null=True,blank=True)
    size = models.CharField(max_length=100,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    gender = models.CharField(choices=Config.GENDER,max_length=100,default=Config.Male)
    description = models.CharField(max_length=100,null=True,blank=True)
    price = models.PositiveIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='uploads/')
    status = models.CharField(
        max_length=100, choices=Config.STATUS, default=Config.Available)

    def __str__(self):
        return "%s %s" % (self.name, self.color)

    def get_absolute_url(self):
        return reverse("product_list")

