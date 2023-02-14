from urllib import request
from .models import Customer
from django.urls import reverse_lazy
from datetime import datetime
from seller.models import Seller
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import formset_factory
from .models import Booking,BookedProduct
from .forms import CustomerForm,  BookingForm, BookedProductForm, BookingReturnForm
from django.contrib import  messages
from config.config import  Config
# from django.contrib.auth.decorators import  permission_required
from  django.contrib.auth.mixins import  LoginRequiredMixin
import json
from django.db.models import Q
from catalouge.models import Product
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



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

@login_required
# @permission_required('booking.user_create_booking')
def booking_create(request):
    seller = Seller.objects.get(user = request.user)
    bookingForm = BookingForm()
    customerForm = CustomerForm()
    ProductFormSet = formset_factory(BookedProductForm, extra=2)
    formset = ProductFormSet()
    context = {'bookingForm': bookingForm, 'formset': formset,'customerForm':customerForm}
    if request.method == "POST":
        products = request.POST.getlist("products")
        description = request.POST.getlist("description")
        price = request.POST.getlist("price")
        size = request.POST.getlist("size")
        bookingForm = BookingForm(request.POST)
        customerForm = CustomerForm(request.POST)
        if bookingForm.is_valid() and customerForm.is_valid():
            customer = customerForm.save()
            booking = bookingForm.save(commit=False)
            booking.customer = customer
            booking.seller = seller
            booking.shop = seller.shop
            booking.save()
            bookingForm.save_m2m()
            for x in range(len(products)):
                product = Product.objects.get(id=products[x])
                product.status = Config.Booked
                product.save()
                # booking.products.add(product)
                # booking.save()
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
        context['seller'] = Seller.objects.get(user=request.user)
        context['bookingForm'].startDate = startDate
        return render(request, "booking/booking_create.html", context)
        
class BookingList(LoginRequiredMixin, ListView):
    # permission_required = ('booking:user_view_booking')
    paginate_by = 20
    context_object_name = "booking_list"
    def post(self,request):
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        bookings = Booking.objects.filter( startDate__range=[startDate,endDate]).exclude(status=Config.Returned)
        # return  HttpResponse(endDate)
        context = {
            'startDate':startDate,
            'endDate':endDate,
            'booking_list':bookings
        }
        return  render(request,'booking/booking_list.html',context)

    def get(self,request):
        bookings = Booking.objects.all().exclude(status=Config.Returned)
        context = {
            'booking_list': bookings
        }
        return render(request, 'booking/booking_list.html', context)

# @permission_required('booking.user_view_booking')
def booking_details(request,pk):
    booking = Booking.objects.get(id=pk)
    booked_product_list = BookedProduct.objects.filter(booking=pk)
    context ={
        'booking':booking,
        'booked_product_list':booked_product_list
    }
    return render(request,'booking/booking_details.html',context)

# @permission_required('booking.user_update_booking')
def booking_update(request, pk):
    booking = Booking.objects.get(id=pk)
    booked_product_list = BookedProduct.objects.filter(booking=pk,product__in=booking.products.all())
    if request.method == 'POST':
        data = request.POST
        total = booking.totalAmount 
        data.getlist('booked_product')
        for prod in data.getlist('booked_product'):
            product = Product.objects.get(id=prod)
            product.status = Config.Available
            product.save()
            booking.products.remove(product)
            total -= product.price
        amount_paid = data['amountPaid']
        booking.amountPaid = amount_paid
        amount_due = total-int(amount_paid)
        if booking.products.count() == 0:
            booking.status = Config.Returned
        booking.save()
        return redirect('booking_list')
    context ={
        'booking':booking,
        'booked_product_list':booked_product_list
    }
    return render(request,'booking/return_booking.html',context)


# @permission_required('booking.user_delete_booking')
def booking_delete(request, pk):
    booking = Booking.objects.get(id=pk)
    if request.method == 'POST':
        for prod in booking.products.all():
            prod.status = Config.Available
            prod.save()
        booking.delete()
        return redirect('booking_list')
    context = {
        'booking':booking,
    }
    return render(request,'booking/booking_delete.html',context)

# @permission_required('booking.user_view_booking')
def return_list(request):
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        return_list = Booking.objects.filter(startDate__range=[startDate,endDate],status=Config.Returned)
        # return_list = Booking.objects.filter( status=Config.Returned)
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


# @permission_required('booking.user_view_booking')
def pending_list(request):
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        pending_list = Booking.objects.filter(startDate__range=[startDate,endDate]).exclude(status=Config.Returned)
        # pending_list = Booking.objects.filter( status=Config.Returned)
        context = {
            'startDate':startDate,
            'endDate':endDate,
            'pending_list':pending_list
        }
        return render(request, 'booking/pending_list.html', context)
    else:
        pending_list = Booking.objects.all().exclude(status=Config.Returned)
        context = {
                'pending_list':pending_list
        }
        return  render(request,'booking/pending_list.html',context)

# @permission_required('booking.user_view_booking')
def send_list(request):
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        send_list = Booking.objects.filter(startDate__range=[startDate,endDate]).exclude(status=Config.Returned)
    else:
        send_list = Booking.objects.filter(startDate__gte=datetime.today()).exclude(status=Config.Returned)
    context = {
            'send_list':send_list
    }
    return  render(request,'booking/send_list.html',context)

# @permission_required('booking.user_view_booking')
def receive_list(request):
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        receive_list = Booking.objects.filter(endDate__range=[startDate,endDate]).exclude(status=Config.Returned)
    else:
        receive_list = Booking.objects.filter(endDate__gte=datetime.today()).exclude(status=Config.Returned)
    context = {
            'receive_list':receive_list
    }
    return  render(request,'booking/receive_list.html',context)

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
