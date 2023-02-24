
from django.urls import path, include

from .views import *

urlpatterns = [
    # path("register/", login_view, name="register"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout, name="logout"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]
