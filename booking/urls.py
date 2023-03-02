
from django.urls import path, include

from .views import *

urlpatterns = [
    path('search/', booked_product_search, name="booked_product_search"),
    path("booking/", BookingList.as_view(), name="booking_list"),
    path("booking/<int:pk>/", booking_details, name="booking_details"),
    path("booking/search/", booking_search, name="booking_search"),
    path("booking/add/", booking_create, name="booking_add"),
    path("booking/update/<int:pk>/", booking_update, name="booking_update"),
    path("booking/delete/<int:pk>/", booking_delete, name="booking_delete"),
    path("booking/return/", return_list, name="return_list"),
    path("booking/pending/", pending_list, name="pending_list"),
    path("booking/send/", send_list, name="send_list"),
    path("booking/receive/", receive_list, name="receive_list"),
    path("customer/", CustomerList.as_view(), name="customer_list"),
    path("customer/add/", CustomerCreate.as_view(), name="customer_add"),
    path("customer/update/<int:pk>/", CustomerUpdate.as_view(), name="customer_update"),
    path("customer/delete/<int:pk>/", CustomerDelete.as_view(), name="customer_delete"),
    path('pickup/<int:pk>/',pickup,name="pickup")
]
