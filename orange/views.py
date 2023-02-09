from django.shortcuts import render
from django.contrib import  messages
from booking.models import  Booking
from datetime import  date, datetime

from config.config import Config

def dashboard(request):
    template_name = "dashboard.html"
    if request.method=="POST":
        fromDate = datetime.today()
        # toDate = request.POST.get('endDate')
        try:
            toSend = Booking.objects.filter(startDate=fromDate).exclude(status=Config.Returned)
            toRecieve = Booking.objects.filter(endDate=fromDate).exclude(status=Config.Returned)
        except Booking.DoesNotExist:
            toSend = None
            toRecieve = None
        # bookings = Booking.objects.get(startDate=fromDate)
        context ={
            'fromDate':fromDate,
            # 'toDate':toDate,
            'toSend': toSend,
            'toRecieve': toRecieve
        }
        return  render(request,template_name,context)
    try:
        toSend = Booking.objects.filter(startDate__gte=date.today()).exclude(status=Config.Returned)
        toRecieve = Booking.objects.filter(endDate__gte=date.today(),startDate__lte=date.today()).exclude(status=Config.Returned)
    except Booking.DoesNotExist:
        toSend = None
        toRecieve =None
    is_approved = False
    if request.user.is_authenticated and request.user.is_active:
        is_approved = True
    if not is_approved:
        messages.success(
            request, 'An email has been sent to your mail id, please verify your account and then log in!')
    context = {
        'toSend':toSend,
        'toRecieve':toRecieve,
        'is_approved':is_approved
    }
    return  render(request,template_name,context)