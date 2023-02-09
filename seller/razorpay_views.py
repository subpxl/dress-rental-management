from django.shortcuts import redirect, render
from django.contrib import messages
import razorpay
from .models import Subscription
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def plan_paymenthandler(request):
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print('\n\n\n\n\npayment data', params_dict)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print("\n\n\n\nresult verify", result)
            if result:
                try:
                    print("in results ")
                    subscription = Subscription.objects.get(transaction_id=params_dict['razorpay_order_id'])
                    subscription.payment_id =params_dict['razorpay_payment_id']
                    subscription.signature_id=params_dict['razorpay_signature']
                    subscription.status = "Success"
                    subscription.save()
                    messages.success(
                        request, 'Your payment for plan ' + subscription.plan_name + ' of amount $' + str(subscription.amount/100) + ' is successful')
                    return redirect('payment_success')
                except Exception as e:
                    print("\n\n\n Error occured ", e)
                    return render(request, 'paymentfail.html')
            else:
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()