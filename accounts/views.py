from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import login, logout, authenticate
from .utils import send_notification_email
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.views import View
from seller.models import Seller
from django.contrib.sites.shortcuts import get_current_site
from accounts.models import User
from django.contrib import auth, messages

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            auth.login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('dashboard')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('register')


def register(request):
    print("hello user")
    if request.method == "POST":
        bus_name = request.POST.get('bus_name')
        email = request.POST.get('email')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        password = request.POST.get('password')
        # try:
        user = User.objects.create_user(
                first_name = f_name,
                last_name = l_name,
                username = email,
                email=email,
                password=password
            )
        user.role = User.SELLER
        user.save()
        seller = Seller(name=bus_name)
        seller.user = user
        seller.save()
        print('Seller created successfully')
        context_email = {
            'domain':get_current_site(request).domain,
            'user':user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }

        send_notification_email("Verify your email","accounts/emails/approve_email.html",email,context_email)
        return redirect('dashboard')
    return render(request,'accounts/register_page.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            redirect('login')
            messages.info(request, "username or password is incorrect")
    return render(request, "accounts/login_page.html", {})

def logout(request):
    auth.logout(request)
    return redirect('login')