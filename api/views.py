from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import User
from .serializers import RegisterSerializer


class APIRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer