
from django.urls import path, include

from .views import *

urlpatterns = [
    path('search/', booked_product_search, name="booked_product_search"),
    path("booking/", BookingList.as_view(), name="booking_list"),
    path("booking/add/", booking_create, name="booking_add"),
    path("return/", return_list, name="return_list"),
    path("customer/", CustomerList.as_view(), name="customer_list"),
    path("customer/add/", CustomerCreate.as_view(), name="customer_add"),
    path("customer/update/<int:pk>/", CustomerUpdate.as_view(), name="customer_update"),
    path("customer/delete/<int:pk>/", CustomerDelete.as_view(), name="customer_delete"),
]
