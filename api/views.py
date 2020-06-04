from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

from .models import UserInfo, Interest
from .serializers import UserInfoSerializer, InterestSerializer


class UserInfoList(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class UserInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class InterestList(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
