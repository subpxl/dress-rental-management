from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from . import views

app_name = 'api'
router = routers.DefaultRouter()

urlpatterns = [
     path('login/', TokenObtainPairView.as_view(), name='api_login'),
     path('register/', views.APIRegisterView.as_view(), name='api_register'),
     path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
] 
urlpatterns += router.urls
