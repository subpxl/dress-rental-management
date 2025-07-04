from audioop import reverse
from datetime import datetime
from multiprocessing import context
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import Seller, Subscription, Shop ,Tax_and_Quantity
from django.shortcuts import render, redirect
from django.contrib import  messages
from accounts.tokens import account_activation_token
from .forms import SellerCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
import razorpay
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from accounts.utils import send_notification_email
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from accounts.models import User
from django.contrib.auth.decorators import login_required
from .forms import Tax_and_Quantity_Form

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
    seller_exists=Tax_and_Quantity.objects.filter(seller=seller)
    form=Tax_and_Quantity_Form()
    if request.method=="POST":
        
        if seller_exists:
            form=Tax_and_Quantity_Form(request.POST,instance=seller_exists[0])
            if form.is_valid():
                form.save()
        else:
            form=Tax_and_Quantity_Form(request.POST)
            if form.is_valid():
                save_form=form.save(commit=False)
                save_form.seller=seller
                save_form.save()

        return redirect('seller_profile')

    if seller_exists:
        form=Tax_and_Quantity_Form(instance=seller_exists[0])
    context = {'seller':seller,'form':form}
    return render(request,'seller/profile.html',context)
        
def staff_create(request):
    if request.method == 'POST':
        form = SellerCreationForm(request.POST)
        if form.is_valid():
            seller_obj = form.save(commit=False)
            email = request.POST.get('email')
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            password = request.POST.get('password')
            user = User.objects.create_user(
                first_name = f_name,
                last_name = l_name,
                username = email,
                email=email,
                password=password
            )
            user.role = User.SELLER
            user.save()
            seller_obj.user = user
            seller_obj.shop = Seller.objects.get(user=request.user).shop
            seller_obj.save()
        
        context_email = {
            'domain':get_current_site(request).domain,
            'user':user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        send_notification_email("Verify your email","accounts/emails/approve_email.html",email,context_email)
        return redirect('staff_list')
    else:
        form = SellerCreationForm()
        context = {
            'form':form,
        }
        return render(request,'seller/staff_create.html',context)

def staff_update(request, pk):
    seller = Seller.objects.get(id=pk)
    if request.method == 'POST':
        form = SellerCreationForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
        return redirect('staff_list')
    else:
        form = SellerCreationForm(instance=seller)
        context = {
            'form':form,
        }
        return render(request,'seller/staff_create.html',context)

@login_required
def create_profile(request):
    seller = Seller.objects.get(user=request.user)
    if request.method == 'POST':
        form = SellerCreationForm(request.POST, instance=seller)
        if form.is_valid():
            print(form.cleaned_data['role'])
            if form.cleaned_data['role'] == 'ShopAdmin':
                request.user.has_perm('booking.user_view_booking')
                request.user.has_perm('booking.user_update_booking')
                request.user.has_perm('booking.user_create_booking')
                request.user.has_perm('booking.user_delete_booking')
            form.save()
        return redirect('seller_profile')
    else:
        form = SellerCreationForm(instance=seller)
        context = {
            'form':form,
        }
    return render(request,'seller/create_profile.html',context)

class StaffList(ListView):
    # permission_required = ('users.view_user')
    model = Seller
    template_name = 'seller/staff_list.html'

    def get(self,request):
        shop = Seller.objects.get(user=request.user).shop
        staff_list = Seller.objects.filter(shop=shop)
        context ={
            "staff_list":staff_list
        }
        return render(request,'seller/staff_list.html',context)

class StaffDelete(DeleteView):
    # permission_required = ('users.delete_user')
    model = Seller
    template_name = "seller/staff_delete.html"
    success_url = reverse_lazy('staff_list')

class StaffDetails(DetailView):
    # permission_required = ('users.view_user')
    model = Seller
    template_name = 'seller/staff_details.html'

# class BranchList(ListView):
#     # permission_required = ('users.view_user')
#     model = Branch
#     template_name = 'seller/branch_list.html'

#     def get(self,request):
#         shop = Seller.objects.get(user=request.user).shop
#         branch_list = Branch.objects.filter(main_shop=shop)
#         context ={
#             "branch_list":branch_list
#         }
#         return render(request,'seller/branch_list.html',context)

# def branch_create(request):
#     if request.method == 'POST':
#         form = BranchCreationForm(request.POST)
#         if form.is_valid():
#             branch_obj = form.save(commit=False)
#             branch_obj.main_shop = Seller.objects.get(user=request.user).shop
#             branch_obj.save()
#         else:
#             messages.info(request, form.errors)
#             return redirect('branch_create')
#         return redirect('branch_list')
#     else:
#         form = BranchCreationForm()
#         context = {
#             'form':form,
#         }
#         return render(request,'seller/branch_create.html',context)

# def branch_update(request,pk):
#     branch = Branch.objects.get(id=pk)
#     if request.method == 'POST':
#         form = BranchCreationForm(request.POST,instance=branch)
#         if form.is_valid():
#             form.save()
#         else:
#             messages.info(request, form.errors)
#             return redirect('branch_update', branch.pk)
#         return redirect('branch_list')
#     else:
#         form = BranchCreationForm(instance=branch)
#         context = {
#             'form':form,
#         }
#         return render(request,'seller/branch_create.html',context)

# class BranchDelete(DeleteView):
#     # permission_required = ('users.delete_user')
#     model = Branch
#     template_name = "seller/branch_delete.html"
#     success_url = reverse_lazy('branch_list')

# class BranchDetails(DetailView):
#     # permission_required = ('users.view_user')
#     model = Branch
#     template_name = 'seller/branch_details.html'