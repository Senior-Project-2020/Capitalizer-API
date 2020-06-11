from rest_framework import generics, permissions

from .models import Interest
from .serializers import InterestSerializer

class InterestList(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]