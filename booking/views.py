from urllib import request
from .models import Customer
from django.urls import reverse_lazy
from datetime import datetime
from seller.models import Seller,Shop,Tax_and_Quantity
from django.core.paginator import Paginator
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
from datetime import date
from seller.forms import Tax_and_Quantity_Form
from django.http import JsonResponse
@csrf_exempt
def booked_product_search(request):
    if request.method == "POST":
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        startTime = request.POST.get('startTime')
        endTime = request.POST.get('endTime')
        # branch = request.POST.get('branch')
        # print("testing ------")
        # test = Booking.objects.get(id=4)
        # print(test.startDate, test.startTime, test.endDate, test.endTime)
        # print(startDate, startTime, endDate, endTime)
        # same_times = Booking.objects.filter(startTime__gte=startTime)
        # print(same_times)
        # black_list = BookedProduct.objects.filter(
        #                 Q(booking__startDate__lt=endDate)|Q(booking__startDate=endDate,booking__startTime__lte=endTime),
        #                 Q(booking__endDate__gt=startDate)|Q(booking__endDate=startDate,booking__endTime__gte=startTime)|Q(status='Booked')|Q(status='Maintainence')
        #             ).values_list('product',flat=True).distinct()
        # black_list = BookedProduct.objects.filter(
        #             Q(status='Booked')|Q(status='Maintainence')
        #             ).values_list('product',flat=True).distinct()
        black_list = BookedProduct.objects.filter(
                        Q(status='Booked')|Q(status='Maintainence'),
                        Q(booking__startDate__lte=endDate),
                        Q(booking__endDate__gte=startDate)
                    ).values_list('product',flat=True).distinct()
        print("blacklist:{}".format(black_list))
        found_product = Product.objects.filter(Q(status='Available')|Q(status="Returned"),shop__seller__user = request.user).exclude(id__in=black_list).values()
        list_of_dicts = list(found_product)
        # print(list_of_dicts,"1")
        data = json.dumps(list_of_dicts)
        return HttpResponse(data, content_type="application/json")
    else:
        found_product = Product.objects.filter(status='Available').values()
        list_of_dicts = list(found_product)
        print(list_of_dicts,"1")
        data = json.dumps(list_of_dicts)
        return HttpResponse(data, content_type="application/json")

@login_required
# @permission_required('booking.user_create_booking')
def booking_create(request):
    seller = Seller.objects.get(user = request.user)
    check=Tax_and_Quantity.objects.filter(seller=seller)
    check_tax_quantity=None
    if check:
        check_tax_quantity=check[0]
    # print(check_tax_quantity.consider_quantity)
    bookingForm = BookingForm()
    customerForm = CustomerForm()
    ProductFormSet = formset_factory(BookedProductForm, extra=2)
    formset = ProductFormSet()
    # if request.is_ajax():
    #     val=request.GET.get('term')
    #     print(val)
    context = {'bookingForm': bookingForm, 'formset': formset,'customerForm':customerForm,'check_tax_quantity':check_tax_quantity}
    if request.method == "POST":
        products = request.POST.getlist("products")
        description = request.POST.getlist("description")
        price = request.POST.getlist("price")
        size = request.POST.getlist("size")
        bookingForm = BookingForm(request.POST)
        customerForm = CustomerForm(request.POST)
        # branch_id = int(request.POST.get('branch'))
        if bookingForm.is_valid() and customerForm.is_valid():
            customer = customerForm.save()
            booking = bookingForm.save(commit=False)
            booking.customer = customer
            booking.shop = Shop.objects.get(seller__user=request.user)
            booking.seller = seller
            booking.orderNo = (booking.shop.name[:4] + booking.orderNo).upper()
            booking.save()
            bookingForm.save_m2m()
            for x in range(len(products)):
                # product = Product.objects.filter(Q(id=products[x]))
                # product.status = Config.Booked
                # product.save()
                bookedProduct = BookedProduct(booking=booking,product_id=products[x],description=description[x],price=price[x],size=size[x],status=Config.Booked)
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
        
class BookingList(ListView):
    model = Booking
    def post(self,request):
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        bookings = Booking.objects.filter(seller__user=request.user,startDate__gte=startDate,endDate__lte=endDate).exclude(status=Config.Returned)
        # return  HttpResponse(endDate)
        context = {
            'startDate':startDate,
            'endDate':endDate,
            'booking_list':bookings
        }
        return  render(request,'booking/booking_list.html',context)

    def get(self,request):
        bookings = Booking.objects.filter(seller__user=request.user).exclude(Q(status=Config.Returned)|Q(status=Config.PickedUp))
        paginator = Paginator(bookings, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'booking_list': bookings,
            'page_obj':page_obj,
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

def booking_search(request):
    if request.method == 'POST':
        pk = request.POST.get('id_booking_pk')
        booking = Booking.objects.get(orderNo=pk)
        booked_product_list = BookedProduct.objects.filter(booking=booking)
        context ={
            'booking':booking,
            'booked_product_list':booked_product_list
        }
        return render(request,'booking/booking_details.html',context)
    return redirect('booking_list')

# @permission_required('booking.user_update_booking')
def booking_update(request, pk):
    booking = Booking.objects.get(id=pk)
    booked_product_list = BookedProduct.objects.filter(Q(status=Config.Booked)|Q(status=Config.PickedUp),booking=pk)
    if request.method == 'POST':
        
        data = request.POST
        total = booking.totalAmount 
        data.getlist('booked_product')
        for prod in data.getlist('booked_product'):
            product = BookedProduct.objects.get(product__id=prod,booking__id=pk)
            # if Booking.objects.filter(prodcuts=product).count()==0:
            product.status = Config.Returned
            product.save()
            # booking.products.remove(product)
            # total -= product.price
        booking.final_paid = data['final_paid']
        # booking.amountPaid = total-int(amount_due)-int(booking.discount)
        if BookedProduct.objects.filter(booking__id=pk,status=Config.Booked).count() == 0:
            print(booking)
            booking.status = Config.Returned
        # booking.endDate=date.today()
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
        for prod in booking.bookedproduct_set.all():
            prod.status = Config.Returned
            prod.save()
        booking.delete()
        return redirect('booking_list')
    context = {
        'booking':booking,
    }
    return render(request,'booking/booking_delete.html',context)

# @permission_required('booking.user_view_booking')
def return_list(request):
    seller = Seller.objects.get(user = request.user)
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        return_list = Booking.objects.filter(seller=seller,startDate__gte=startDate,endDate__lte=endDate,status=Config.Returned)
        # return_list = Booking.objects.filter( status=Config.Returned)
        paginator = Paginator(return_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj':page_obj,
            'startDate':startDate,
            'endDate':endDate,
            'return_list':return_list
        }
        return render(request, 'booking/return_list.html', context)
    else:
        return_list = Booking.objects.filter(seller=seller,status=Config.Returned)
        paginator = Paginator(return_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
                'page_obj':page_obj,
                'return_list':return_list
        }
        return  render(request,'booking/return_list.html',context)


# @permission_required('booking.user_view_booking')
def pending_list(request):
    seller = Seller.objects.get(user = request.user)
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        pending_list = Booking.objects.filter(seller=seller,startDate__gte=startDate,endDate__lte=endDate).exclude(status=Config.Returned)
        paginator = Paginator(pending_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj':page_obj,
            'startDate':startDate,
            'endDate':endDate,
            'pending_list':pending_list
        }
        return render(request, 'booking/pending_list.html', context)
    else:
        pending_list = Booking.objects.filter(seller=seller,bookedproduct__status=Config.Returned).exclude(status=Config.Returned)
        paginator = Paginator(pending_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj':page_obj,
            'pending_list':pending_list
        }
        return  render(request,'booking/pending_list.html',context)

# @permission_required('booking.user_view_booking')
def send_list(request):
    seller = Seller.objects.get(user = request.user)
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        send_list = Booking.objects.filter(seller=seller,startDate__gte=datetime.today(),endDate__lte=endDate).exclude(status=Config.Returned)
    else:
        send_list = Booking.objects.filter(seller=seller,startDate__gte=datetime.today()).exclude(status=Config.Returned)
    paginator = Paginator(send_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
            'page_obj':page_obj,
            'send_list':send_list
    }
    return  render(request,'booking/send_list.html',context)

# @permission_required('booking.user_view_booking')
def receive_list(request):
    seller = Seller.objects.get(user = request.user)
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        receive_list = Booking.objects.filter(seller=seller,startDate__gte=startDate,endDate__lte=datetime.today()).exclude(status=Config.Returned)
    else:
        receive_list = Booking.objects.filter(seller=seller,endDate__lte=datetime.today()).exclude(status=Config.Returned)
    paginator = Paginator(receive_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
            'page_obj':page_obj,
            'receive_list':receive_list
    }
    return  render(request,'booking/receive_list.html',context)

class CustomerList(ListView):
    paginate_by = 20
    model = Customer
    template_name = 'customer/customer_list.html'

    def get(self,request):
        seller = Seller.objects.get(user=request.user)
        bookings = Booking.objects.filter(seller=seller)
        context ={
            "customer_list":bookings
        }
        return render(request,'customer/customer_list.html',context)


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

def pickup(request,pk):
    booking = Booking.objects.get(id=pk)
    booked_product_list = BookedProduct.objects.filter(booking=pk,status=Config.Booked)
    if request.method == 'POST':
        
        data = request.POST
        total = booking.totalAmount 
        data.getlist('booked_product')
        for prod in data.getlist('booked_product'):
            product = BookedProduct.objects.get(product__id=prod,booking__id=pk)
            # if Booking.objects.filter(prodcuts=product).count()==0:
            product.status = Config.PickedUp
            product.save()
            # booking.products.remove(product)
            # total -= product.price
        booking.final_paid = data['final_paid']
        # booking.amountPaid = total-int(amount_due)-int(booking.discount)
        if BookedProduct.objects.filter(booking__id=pk,status=Config.Booked).count() == 0:
            print(booking)
            booking.status = Config.PickedUp
        booking.save()
        return redirect('booking_list')
    context ={
        'booking':booking,
        'booked_product_list':booked_product_list
    }
    return render(request,'booking/pickup.html',context=context)

# def pickup(request, pk):
#     booking = Booking.objects.get(id=pk)
#     booked_product_list = BookedProduct.objects.filter(booking=pk,status=Config.Booked)
#     if request.method == 'POST':
        
#         data = request.POST
#         total = booking.totalAmount 
#         data.getlist('booked_product')
#         for prod in data.getlist('booked_product'):
#             product = BookedProduct.objects.get(product__id=prod,booking__id=pk)
#             # if Booking.objects.filter(prodcuts=product).count()==0:
#             product.status = Config.Returned
#             product.save()
#             # booking.products.remove(product)
#             # total -= product.price
#         booking.final_paid = data['final_paid']
#         # booking.amountPaid = total-int(amount_due)-int(booking.discount)
#         if BookedProduct.objects.filter(booking__id=pk,status=Config.Booked).count() == 0:
#             print(booking)
#             booking.status = Config.Returned
#         booking.endDate=date.today()
#         booking.save()
#         return redirect('booking_list')
#     context ={
#         'booking':booking,
#         'booked_product_list':booked_product_list
#     }
#     return render(request,'booking/return_booking.html',context)


def pickup_list(request):
    seller = Seller.objects.get(user = request.user)
    if request.method=="POST":
        startDate = request.POST.get("startDate","")
        endDate = request.POST.get("endDate","")
        pick_up_list = Booking.objects.filter(seller=seller,startDate__gte=startDate,endDate__lte=endDate,status=Config.PickedUp)
        # return_list = Booking.objects.filter( status=Config.Returned)
        paginator = Paginator(pick_up_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj':page_obj,
            'startDate':startDate,
            'endDate':endDate,
            'pick_up_list':pick_up_list
        }
        return render(request, 'booking/return_list.html', context)
    else:
        pick_up_list  = Booking.objects.filter(seller=seller,status=Config.PickedUp)
        print(pick_up_list,'pi')
        paginator = Paginator(pick_up_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
                'page_obj':page_obj,
                'pick_up_list':pick_up_list
        }
        return  render(request,'booking/pickup_list.html',context)


def tax_configurations(request):
    form=Tax_and_Quantity_Form()
    seller = Seller.objects.get(user = request.user)
    tax_data=Tax_and_Quantity.objects.filter(seller=seller)
    if request.method=="POST":
        form=Tax_and_Quantity_Form(request.POST)
        if form.is_valid():
            save_form=form.save(commit=False)
            save_form.seller=seller
            save_form.save()
            return redirect('tax_configurations')

    context={'form':form,'tax_data':tax_data}
    return render(request,'includes/tax_configurations.html',context)

def delete_tax(request,pk):
    tax_data=Tax_and_Quantity.objects.get(id=pk)
    tax_data.delete()
    return redirect('tax_configurations')


def get_tax_dropdown_data(request):
    taxes=Tax_and_Quantity.objects.filter(seller__user=request.user).values()
    values = list(taxes)
    # data=json.dumps(taxes)
    return JsonResponse(values,safe=False)

def edit_tax(request,pk):
    taxes=Tax_and_Quantity.objects.get(id=pk)
    form=Tax_and_Quantity_Form(instance=taxes)
    if request.method=="POST":    
        form=Tax_and_Quantity_Form(request.POST,instance=taxes)
        if form.is_valid():
            form.save()
            return redirect('tax_configurations')
    context={
        'form':form
    }

    return render(request,'includes/edit_tax.html',context)
    
    
