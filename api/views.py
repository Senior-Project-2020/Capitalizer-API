from rest_framework import generics

from .models import Interest
from .serializers import InterestSerializer

class InterestList(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
