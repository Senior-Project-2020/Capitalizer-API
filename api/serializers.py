from rest_framework import serializers

from .models import PCUser, Interest

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'interest']

class PCUserDetailSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(many=True, queryset=Interest.objects.all())

    class Meta:
        model = PCUser
        fields = ['id', 'username', 'email', 'interests']