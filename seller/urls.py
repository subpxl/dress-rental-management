
from django.urls import path, include

from .views import *

urlpatterns = [
    path("shop/", ShopList.as_view(), name="shop_list"),
    path("shop/<int:pk>/", ShopDetails.as_view(), name="shop_details"),
    path("shop/create/", ShopCreate.as_view(), name="shop_create"),
    path("shop/update/<int:pk>/", ShopUpdate.as_view(), name="shop_update"),
    path("shop/delete/<int:pk>/", ShopDelete.as_view(), name="shop_delete"),
    path("staff/",StaffList.as_view(),name="staff_list"),
    path("staff/create/",StaffCreate.as_view(),name="staff_create"),
    path("staff/<int:pk>/", StaffDetails.as_view(), name="staff_details"),
    path("staff/update/<int:pk>/",StaffUpdate.as_view(),name="staff_update"),
    path("staff/delete/<int:pk>/", StaffDelete.as_view(), name="staff_delete"),
]
