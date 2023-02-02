
from django.urls import path, include

from .views import ShopList, ShopCreate, ShopUpdate, ShopDelete,ShopDetails

urlpatterns = [
    path("", ShopList.as_view(), name="shop_list"),
    path("<int:pk>/", ShopDetails.as_view(), name="shop_details"),
    path("create/", ShopCreate.as_view(), name="shop_create"),
    path("update/<int:pk>/", ShopUpdate.as_view(), name="shop_update"),
    path("delete/<int:pk>/", ShopDelete.as_view(), name="shop_delete"),
]
