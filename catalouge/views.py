from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Category, Product
from django.urls import reverse_lazy
from  django.contrib.auth.mixins import PermissionRequiredMixin
# from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
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
