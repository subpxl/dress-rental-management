from django.shortcuts import render
from django.contrib import  messages
from booking.models import  BookedProduct, Booking
from datetime import date as dt, datetime
from config.config import Config
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import timedelta
from seller.models import Seller, Subscription
from catalouge.models import Product

@login_required
def dashboard(request):
    template_name = "dashboard.html"
    is_approved = False
    today = datetime.today().strftime("%d %b, %Y - %A")
    print(today)
    if request.user.is_authenticated and request.user.is_active:
        is_approved = True
    if not is_approved:
        return render(request,template_name)
    seller = Seller.objects.get(user = request.user)
    revenue = 0
    data = [
        {
            'name':'Bookings',
            'value':0
        },
        {
            'name':'Pendings',
            'value':0
        },
        {
            'name':'Returns',
            'value':0
        }
    ]
    try:
        data[0]['value']=Booking.objects.filter(seller=seller).exclude(status=Config.Returned).count()
        data[2]['value']=Booking.objects.filter(seller=seller,status=Config.Returned).count()
        data[1]['value']=Booking.objects.filter(seller=seller).count() - data['Bookings'] - data['Returns']
    except:
        pass
    try:
        revenue_list = Booking.objects.filter(seller=seller)
        revenue = revenue_list.aggregate(Sum('amountPaid'))['amountPaid__sum']
        if not revenue:
            revenue = 0
    except:
        pass
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
    
    if request.method=="POST":
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        try:
            toSend = Booking.objects.filter(seller=seller,startDate__gte=dt.today(),endDate__lte=endDate).exclude(status=Config.Returned)
            toRecieve = Booking.objects.filter(seller=seller,startDate__gte=startDate,endDate__lte=dt.today()).exclude(status=Config.Returned)
        except Booking.DoesNotExist:
            toSend = None
            toRecieve = None
        context = {
        'revenue':revenue,
        'data':data,
        'today':today,
        'toSend':toSend,
        'toRecieve':toRecieve,
        'is_approved':is_approved
    }
        return  render(request,template_name,context)
    try:
        toSend = Booking.objects.filter(startDate__gte=dt.today(),seller=seller).exclude(status=Config.Returned)
        toRecieve = Booking.objects.filter(endDate__lte=dt.today(),seller=seller).exclude(status=Config.Returned)
    except Booking.DoesNotExist:
        toSend = None
        toRecieve =None
    context = {
        'revenue':revenue,
        'data':data,
        'today':today,
        'toSend':toSend,
        'toRecieve':toRecieve,
        'is_approved':is_approved
    }
    return render(request,template_name,context)