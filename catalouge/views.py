from math import prod
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Product
from .forms import ProductCreationForm
from seller.models import Seller, Shop, Branch
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
from django.contrib.auth.decorators import login_required


class ProductList(ListView):
    paginate_by = 20
    model = Product

    def get(self,request):
        seller = Seller.objects.get(user=request.user)
        product_list = Product.objects.filter(seller=seller)
        context ={
            "product_list":product_list
        }
        return render(request,'product/product_list.html',context)


class MaintainanceList(ListView):
    paginate_by = 20
    model = Product
    def get(self,request):
        seller = Seller.objects.get(user=request.user)
        product_list = Product.objects.filter(seller=seller,status="maintainance")
        context ={
            "product_list":product_list
        }
        return render(request,'product/maintainance_list.html',context)






@login_required
def product_create(request):
    seller = Seller.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES, initial={'shop':seller.shop})
        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.branch = product_obj.category.branch
            product_obj.seller = seller
            product_obj.save()
            return redirect('product_list')
        else:
            print(form.errors)
            messages.error(request,
                form.errors
            )
            return redirect('product_create')
    form = ProductCreationForm(initial={'shop':seller.shop})
    context = {
        'form':form,
    }
    return render(request,'product/product_create.html',context)

@login_required
def product_update(request, pk):
    seller = Seller.objects.get(user=request.user)
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            print(form.errors)
            messages.error(request,
                form.errors
            )
            return redirect('product_update', product.pk)
    form = ProductCreationForm(instance=product)
    context = {
        'form':form,
        'product':product,
    }
    return render(request,'product/product_create.html',context)

@login_required
def product_search(request):
    product = request.GET.get('product')
    try:
        product =Product.objects.get(tag=product)
        return redirect('product_detail', product.pk)
    except:
        messages.error(request, f"{product} tag not found")
        return redirect('product_list')



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
            seller = Seller.objects.get(name=column[5])
            image = urllib.request.urlretrieve(column[8])
            product = Product.objects.update_or_create(
                tag=column[0],
                name=column[1],
                category_id=category.id,
                color=column[3],
                size=column[4],
                branch_id=category.branch.id,
                seller_id=seller.id,
                gender=column[6],
                description=column[7],
                price=column[9],
            )
            product[0].image.save(
                os.path.basename(column[1]),
                File(open(image[0], 'rb'))
            )
            product[0].save()
        return  redirect('product_list')
    return  render(request,"product/bulk_upload.html")


class CategoryList(ListView):
    paginate_by = 20
    model = Category

    def get(self,request):
        shop = Seller.objects.get(user=request.user).shop
        category_list = Category.objects.filter(branch__main_shop=shop)
        context ={
            "category_list":category_list
        }
        return render(request,'category/category_list.html',context)

class CategoryCreate( CreateView):
    # permission_required = ('category.create_category')
    model = Category
    fields = "__all__"
    template_name = "category/category_create.html"

    def get_form(self, *args, **kwargs):
        form = super(CategoryCreate, self).get_form(*args, **kwargs)
        seller = Seller.objects.get(user = self.request.user)
        form.fields['branch'].queryset = Branch.objects.filter(main_shop=seller.shop)
        return form

class CategoryUpdate( UpdateView):
    # permission_required = ('category.update_category')
    model = Category
    fields = "__all__"
    template_name = "category/category_create.html"

    def get_form(self, *args, **kwargs):
        form = super(CategoryUpdate, self).get_form(*args, **kwargs)
        seller = Seller.objects.get(user = self.request.user)
        form.fields['branch'].queryset = Branch.objects.filter(main_shop=seller.shop)
        return form

class CategoryDelete( DeleteView):
    # permission_required = ('category.delete_category')
    model = Category
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('category_list')
