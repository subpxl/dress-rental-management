from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import Shop
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