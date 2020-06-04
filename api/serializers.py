from rest_framework import serializers
#from django.contrib.auth.models import User

from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['email', 'interests']