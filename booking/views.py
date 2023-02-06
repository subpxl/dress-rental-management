from .models import Customer
from django.urls import reverse_lazy
import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import formset_factory
from .models import Booking,BookedProduct
from .forms import  BookingForm,BookedProductForm
from django.contrib import  messages
from config.config import  Config
from django.contrib.auth.decorators import  permission_required
from  django.contrib.auth.mixins import PermissionRequiredMixin
import json
from catalouge.models import Product
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def booked_product_search(request):
    if request.method == "POST":
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        # found_product = Product.objects.exclude(
        #     ( Q(booking__startDate__gte=startDate) & Q(booking__startDate__lte=endDate)
        #     | Q(booking__endDate__lte=endDate) & Q(booking__startDate__gte=startDate))
        #     | Q(status__contains=Config.NotAvailable)
        # ).values()

        found_product = Product.objects.filter(status='Available').values()
        list_of_dicts = list(found_product)
        data = json.dumps(list_of_dicts)
        return HttpResponse(data, content_type="application/json")

    else:
        found_product = Product.objects.filter(status='Available').values()
        list_of_dicts = list(found_product)
        data = json.dumps(list_of_dicts)
        return HttpResponse(data, content_type="application/json")

# @permission_required('booking.create_booking')
def booking_create(request):
    bookingForm = BookingForm()
    ProductFormSet = formset_factory(BookedProductForm, extra=2)
    formset = ProductFormSet()
    context = {'bookingForm': bookingForm, 'formset': formset}
    if request.method == "POST":
        products = request.POST.getlist("products")
        description = request.POST.getlist("description")
        price = request.POST.getlist("price")
        size = request.POST.getlist("size")
        bookingForm = BookingForm(request.POST)

        if bookingForm.is_valid():
            booking = bookingForm.save()
            for x in range(len(products)):
                product = Product.objects.get(id=products[x])
                product.status = 'Booking'
                product.save()
                bookedProduct = BookedProduct(booking=booking,product_id=products[x],description=description[x],price=price[x],size=size[x])
                bookedProduct.save()

            # bookingDetails = '/booking/{}'.format(booking.id)
            return redirect('booking_list')
        else:
            messages.info(request, bookingForm.errors)
            return render(request, "booking/booking_create.html", context)
    else:
        startDate =request.GET.get("startDate")
        endDate =request.GET.get("endDate")
        print(startDate ,"   ",endDate)
        context['bookingForm'].startDate = startDate
        return render(request, "booking/booking_create.html", context)

class BookingList(ListView):
    # permission_required = ('booking:view_booking')
    paginate_by = 20
    context_object_name = "booking_list"
    def post(self,request):
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        bookings = Booking.objects.filter( startDate__range=[startDate,endDate])
        # return  HttpResponse(endDate)
        context = {
            'startDate':startDate,
            'endDate':endDate,
            'booking_list':bookings
        }
        return  render(request,'booking/booking_list.html',context)

    def get(self,request):
        bookings = Booking.objects.filter(status=Config.Booking)
        context = {
            'booking_list': bookings
        }
        return render(request, 'booking/booking_list.html', context)
        
def return_list(request):
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        # return_list = Booking.objects.filter( startDate__range=[startDate,endDate],status=Config.Returned)
        return_list = Booking.objects.filter( status=Config.Returned)
        context = {
            'startDate':startDate,
            'endDate':endDate,
            'return_list':return_list
        }
        return render(request, 'booking/return_list.html', context)
    else:
        return_list = Booking.objects.filter(status=Config.Returned)
        context = {
                'return_list':return_list
        }
        return  render(request,'booking/return_list.html',context)

class CustomerList(ListView):
    model = Customer
    context_object_name = "customer_list"
    template_name = 'customer/customer_list.html'


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
