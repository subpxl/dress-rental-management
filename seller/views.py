from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import Shop, Seller
from django.shortcuts import render
from .forms import SellerCreationForm
from django.urls import reverse_lazy
from  django.contrib.auth.mixins import PermissionRequiredMixin

class ShopList(ListView):
    # permission_required = ('shop.view_shop')
    model = Shop
    context_object_name = "shop_list"
    template_name = 'shop/shop_list.html'


class ShopCreate(CreateView):
    # permission_required = ('shop.create_shop')
    model = Shop
    fields = "__all__"
    template_name = "shop/shop_create.html"


class ShopUpdate(UpdateView):
    # permission_required = ('shop.update_shop')
    model = Shop
    fields = "__all__"
    template_name = "shop/shop_create.html"

class ShopDelete(DeleteView):
    # permission_required = ('shop.delete_shop')
    model = Shop
    template_name = 'shop/shop_delete.html'
    success_url = reverse_lazy('shop_list')


class ShopDetails(DetailView):
    # permission_required = ('shop.view_shop')
    model = Shop
    template_name = 'shop/shop_details.html'

class StaffList(ListView):
    # permission_required = ('users.view_user')
    model = Seller
    template_name = 'seller/staff_list.html'

    def get(self,request):
        staff_list = Seller.objects.all()
        context ={
            "staff_list":staff_list
        }
        return render(request,'seller/staff_list.html',context)
        
class StaffCreate(CreateView):
    # permission_required = ('users.create_user')
    model = Seller
    form_class = SellerCreationForm
    template_name = 'seller/staff_create.html'
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StaffUpdate(UpdateView):
    # permission_required = ('users.update_user')
    model = Seller
    form_class = SellerCreationForm
    template_name = "seller/staff_create.html"
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StaffDelete(DeleteView):
    # permission_required = ('users.delete_user')
    model = Seller
    template_name = "seller/staff_delete.html"
    success_url = reverse_lazy('staff_list')

class StaffDetails(DetailView):
    # permission_required = ('users.view_user')
    model = Seller
    template_name = 'seller/staff_details.html'
