
from django.urls import path, include

from .views import CustomerList, CustomerCreate, CustomerUpdate, CustomerDelete

urlpatterns = [

    path("customer/", CustomerList.as_view(), name="customer_list"),
    path("customer/add/", CustomerCreate.as_view(), name="customer_add"),
    path("customer/update/<int:pk>/", CustomerUpdate.as_view(), name="customer_update"),
    path("customer/delete/<int:pk>/", CustomerDelete.as_view(), name="customer_delete"),
]
