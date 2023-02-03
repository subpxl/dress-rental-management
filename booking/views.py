from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Customer
from django.urls import reverse_lazy


class CustomerList(ListView):
    model = Customer
    context_object_name = "customer_list"
    template_name = 'customer/../templates/booking/customer_list.html'


class CustomerCreate(CreateView):
    model = Customer
    fields = "__all__"
    template_name = "customer/customer_create.html"


class CustomerUpdate(UpdateView):
    model = Customer
    fields = "__all__"
    template_name = "customer/customer_create.html"


class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'customer/customer_delete.html'
    success_url = reverse_lazy('customer_list')
