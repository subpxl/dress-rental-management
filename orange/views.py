from django.shortcuts import render
from booking.models import  Booking
from datetime import  date

def dashboard(request):
    template_name = "dashboard.html"
    if request.method=="POST":
        fromDate = request.POST.get('startDate')
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
        toSend = Booking.objects.filter(startDate=date.today())
        toRecieve = Booking.objects.filter(endDate=date.today())
    except Booking.DoesNotExist:
        toSend = None
        toRecieve =None

    context = {
        'toSend':toSend,
        'toRecieve':toRecieve
    }
    return  render(request,template_name,context)