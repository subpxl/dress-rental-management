from math import prod
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Product
from booking.models import Shop
from django.urls import reverse_lazy
from  django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files import File
# from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
import csv
import io
import urllib
import os
from django.contrib import messages
from booking.models import Booking

class ProductList(ListView):
    paginate_by = 20
    model = Product
    context_object_name = "product_list"
    template_name = 'product/product_list.html'


class ProductCreate(CreateView):
    # permission_required = ('product.create_product')
    model = Product
    fields = "__all__"
    template_name = "product/product_create.html"

class ProductUpdate(UpdateView):
    # permission_required = ('product.update_product')
    model = Product
    fields = "__all__"
    template_name = "product/product_create.html"


class ProductDelete(DeleteView):
    # permission_required = ('product.delete_product')
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('product_list')


# @permission_required('product.view_product')
def product_details(request,pk):
    product = Product.objects.get(id=pk)
    bookings = Booking.objects.filter(products  =pk)
    context = {
        'product':product,
        'bookings':bookings
    }
    return  render(request,'product/product_details.html',context)

# @permission_required('product.create_product')
def product_bulk_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if not myfile.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = myfile.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            print(column[0],column[1],column[2],column[3],column[4],column[5],column[6],column[7],column[8],column[9])
            category = Category.objects.get(name=column[2])
            shop = Shop.objects.get(name=column[5])
            image = urllib.request.urlretrieve(column[8])
            product = Product.objects.update_or_create(
                tag=column[0],
                name=column[1],
                category_id=category.id,
                color=column[3],
                size=column[4],
                shop_id=shop.id,
                gender=column[6],
                description=column[7],
                price=column[9],
            )
            print(product[0])
            product[0].image.save(
                os.path.basename(column[1]),
                File(open(image[0], 'rb'))
            )
            product[0].save()
        return  redirect('product_list')
    return  render(request,"product/bulk_upload.html")


class CategoryList(ListView):
    model = Category
    context_object_name = "category_list"
    template_name = 'category/category_list.html'

class CategoryCreate( CreateView):
    # permission_required = ('category.create_category')
    model = Category
    fields = "__all__"
    template_name = "category/category_create.html"


class CategoryUpdate( UpdateView):
    # permission_required = ('category.update_category')
    model = Category
    fields = "__all__"
    template_name = "category/category_create.html"


class CategoryDelete( DeleteView):
    # permission_required = ('category.delete_category')
    model = Category
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('category_list')
