from rest_framework import generics

from .models import Interest, StockPrice, Stock
from .serializers import InterestSerializer, StockPriceSerializer, StockSerializer

class InterestList(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

# Create and list all stock prices
class StockPriceList(generics.ListCreateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

# Update and view individual stock prices
class StockPriceDetail(generics.RetrieveUpdateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

# List all stocks
class StockList(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

# View individual stocks
class StockDetail(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer