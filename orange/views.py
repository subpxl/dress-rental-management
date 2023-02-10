from django.shortcuts import render
from django.contrib import  messages
from booking.models import  BookedProduct, Booking
from datetime import  date as dt, datetime
from config.config import Config
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import timedelta
from seller.models import Seller, Subscription
from catalouge.models import Product

def dashboard(request):
    template_name = "dashboard.html"
    is_approved = False
    if request.user.is_authenticated and request.user.is_active:
        is_approved = True
    if not is_approved:
        messages.success(
            request, 'An email has been sent to your mail id, please verify your account and then log in!')
        return render(request,template_name)
    seller = Seller.objects.get(user = request.user)
    revenue_list = BookedProduct.objects.filter(product__shop=seller.shop)
    revenue = revenue_list.aggregate(Sum('price'))['price__sum']
    dates = Booking.objects.order_by('startDate').values('startDate').distinct()
    top_bookings = Booking.objects.order_by('-amountDue').filter(status=Config.Booked)[:5]
    data = {
        'revenue':[],
        'paid':[],
        'due':[],
        'max':0,
        'dates':[]
    }
    try:
        subs = Subscription.objects.get(seller = seller)
        exp_date = subs.created_at + timedelta(days=30)
        if datetime.today().date() > exp_date.date():
            messages.warning(
                    request,"Your " + subs.plan_name + " is expired on " + exp_date.strftime("%d %b, %Y") +
                        ". Please buy a new plan !"
                        "<a href='/plans' style='margin-left:10px'> Click here</a>"
                )
    except Exception as e:
        print("Error ", e)
    for date in dates:
        bookings = Booking.objects.filter(startDate=date['startDate'])
        revenue = bookings.aggregate(Sum('totalAmount'))['totalAmount__sum']
        paid = bookings.aggregate(Sum('amountPaid'))['amountPaid__sum']
        due = bookings.aggregate(Sum('amountDue'))['amountDue__sum']
        data['revenue'].append(revenue)
        data['paid'].append(paid)
        data['due'].append(due)
        data['dates'].append(date['startDate'].strftime("%Y-%m-%d"))
        data['max'] = max(data['max'],revenue,paid,due)
    if request.method=="POST":
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        try:
            toSend = Booking.objects.filter(startDate__range=[startDate,endDate]).exclude(status=Config.Returned)
            toRecieve = Booking.objects.filter(endDate__range=[startDate,endDate]).exclude(status=Config.Returned)
        except Booking.DoesNotExist:
            toSend = None
            toRecieve = None
        # bookings = Booking.objects.get(startDate=fromDate)
        context = {
        'revenue':revenue,
        'top_bookings':top_bookings,
        'data' : data,
        'toSend':toSend,
        'toRecieve':toRecieve,
        'is_approved':is_approved
    }
        return  render(request,template_name,context)
    try:
        toSend = Booking.objects.filter(startDate__gte=dt.today()).exclude(status=Config.Returned)
        toRecieve = Booking.objects.filter(endDate__gte=dt.today(),startDate__lte=dt.today()).exclude(status=Config.Returned)
    except Booking.DoesNotExist:
        toSend = None
        toRecieve =None
    context = {
        'revenue':revenue,
        'top_bookings':top_bookings,
        'data' : data,
        'toSend':toSend,
        'toRecieve':toRecieve,
        'is_approved':is_approved
    }
    return render(request,template_name,context)