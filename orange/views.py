from django.shortcuts import render
from booking.models import  Booking
from datetime import  date, datetime

def dashboard(request):
    template_name = "dashboard.html"
    if request.method=="POST":
        fromDate = datetime.today()
        # toDate = request.POST.get('endDate')
        try:
            toSend = Booking.objects.filter(startDate=fromDate)
            toRecieve = Booking.objects.filter(endDate=fromDate)
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
        toSend = Booking.objects.filter(startDate__gte=date.today())
        toRecieve = Booking.objects.filter(endDate__lt=date.today())
    except Booking.DoesNotExist:
        toSend = None
        toRecieve =None
    is_approved = False
    if request.user.is_authenticated and request.user.is_active:
        is_approved = True
    context = {
        'toSend':toSend,
        'toRecieve':toRecieve,
        'is_approved':is_approved
    }
    return  render(request,template_name,context)