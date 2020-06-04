from rest_framework import serializers
#from django.contrib.auth.models import User

from .models import UserInfo, Interest

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'interest']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'email', 'interests']