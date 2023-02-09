from datetime import datetime
from multiprocessing import context
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import Shop, Seller, Subscription
from django.shortcuts import render
from .forms import SellerCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
import razorpay
from datetime import datetime
from django.contrib.auth.decorators import login_required

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def plans(request):
    if request.method == 'POST':
        data = request.POST
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        order_number = '#'+str(request.user.id)+'U'+dt_string
        seller = Seller.objects.get(user = request.user)
        try:
            pre_sub = Subscription.objects.get(seller=seller)
            pre_sub.delete()
        except:
            pass
        amount = int(data['amount']) * 100
        plan_name = data['plan_name']
        seller_subscription = Subscription(
            seller = seller,
            order_number = order_number,
            amount = amount,
            plan_name = plan_name,
        )
        data = { "amount": amount, "currency": "INR", "receipt": order_number }
        subs_plan = razorpay_client.order.create(data=data)
        razorpay_order_id = subs_plan['id']
        seller_subscription.transaction_id = razorpay_order_id
        seller_subscription.save()
        request.session['razorpay_order_id'] = razorpay_order_id
        request.session['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        request.session['razorpay_amount'] = amount/100
        context = {
            'plan_name' : plan_name,
            'amount' : amount/100
        }
        return render(request,'seller/buy_plan.html',context)
    return render(request,'seller/plans.html')

def payment_success(request):
    return render(request,'seller/payment_success.html')

class ShopList(ListView):
    # permission_required = ('shop.view_shop')
    model = Shop
    context_object_name = "shop_list"
    template_name = 'shop/shop_list.html'


class ShopCreate(CreateView):
    # permission_required = ('shop.create_shop')
    model = Shop
    fields = "__all__"
    template_name = "shop/shop_create.html"


class ShopUpdate(UpdateView):
    # permission_required = ('shop.update_shop')
    model = Shop
    fields = "__all__"
    template_name = "shop/shop_create.html"

class ShopDelete(DeleteView):
    # permission_required = ('shop.delete_shop')
    model = Shop
    template_name = 'shop/shop_delete.html'
    success_url = reverse_lazy('shop_list')


class ShopDetails(DetailView):
    # permission_required = ('shop.view_shop')
    model = Shop
    template_name = 'shop/shop_details.html'

@login_required
def seller_profile(request):
    seller = Seller.objects.get(user = request.user)
    context = {'seller':seller}
    return render(request,'seller/profile.html',context)

class StaffList(ListView):
    # permission_required = ('users.view_user')
    model = Seller
    template_name = 'seller/staff_list.html'

    def get(self,request):
        staff_list = Seller.objects.all()
        context ={
            "staff_list":staff_list
        }
        return render(request,'seller/staff_list.html',context)
        
class StaffCreate(CreateView):
    # permission_required = ('users.create_user')
    model = Seller
    form_class = SellerCreationForm
    template_name = 'seller/staff_create.html'
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StaffUpdate(UpdateView):
    # permission_required = ('users.update_user')
    model = Seller
    form_class = SellerCreationForm
    template_name = "seller/staff_create.html"
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StaffDelete(DeleteView):
    # permission_required = ('users.delete_user')
    model = Seller
    template_name = "seller/staff_delete.html"
    success_url = reverse_lazy('staff_list')

class StaffDetails(DetailView):
    # permission_required = ('users.view_user')
    model = Seller
    template_name = 'seller/staff_details.html'
