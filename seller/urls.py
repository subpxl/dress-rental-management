
from django.urls import path, include

from .views import *
from .razorpay_views import plan_paymenthandler

urlpatterns = [
    # path("shop/", ShopList.as_view(), name="shop_list"),
    # path("shop/<int:pk>/", ShopDetails.as_view(), name="shop_details"),
    # path("shop/create/", ShopCreate.as_view(), name="shop_create"),
    # path("shop/update/<int:pk>/", ShopUpdate.as_view(), name="shop_update"),
    # path("shop/delete/<int:pk>/", ShopDelete.as_view(), name="shop_delete"),
    path("profile/",seller_profile,name="seller_profile"),
    path("staff/",StaffList.as_view(),name="staff_list"),
    path("staff/create/",staff_create,name="staff_create"),
    path("staff/<int:pk>/", StaffDetails.as_view(), name="staff_details"),
    path("staff/update/<int:pk>/",staff_update,name="staff_update"),
    path("staff/delete/<int:pk>/", StaffDelete.as_view(), name="staff_delete"),
    path('plans/', plans, name='plans'),
    path('payment_success/', payment_success, name='payment_success'),
    path('plan-paymenthandler/', plan_paymenthandler, name='plan_paymentHandler'),
]
