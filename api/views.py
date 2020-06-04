from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

from .models import UserInfo
from .serializers import UserInfoSerializer


class UserInfoList(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class UserInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
