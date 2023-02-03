
from django.urls import path

from .views import *

urlpatterns = [
    path("product/", ProductList.as_view(), name="product_list"),
    path("product/add/", ProductCreate.as_view(), name="product_create"),
    path("product/update/<int:pk>/", ProductUpdate.as_view(), name="product_update"),
    path("product/delete/<int:pk>/", ProductDelete.as_view(), name="product_delete"),
    path("category/", CategoryList.as_view(), name="category_list"),
    path("category/add/", CategoryCreate.as_view(), name="category_create"),
    path("category/update/<int:pk>/", CategoryUpdate.as_view(), name="category_update"),
    path("category/delete/<int:pk>/", CategoryDelete.as_view(), name="category_delete"),
]
