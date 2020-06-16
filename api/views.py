from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .forms import SuggestionDateForm
from .models import Interest, StockPrice, Stock, PCUser
from .serializers import InterestSerializer, StockPriceSerializer, StockSerializer
from .utils import stock_suggestions

class InterestList(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

# List all stock prices; Create reserved for users with special permissions set
class StockPriceList(generics.ListCreateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

# View individual stock prices; Update reserved for users with special permissions set
class StockPriceDetail(generics.RetrieveUpdateAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

# List all stocks; Create reserved for users with special permissions set
class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

# View individual stocks; Update and destroy reserved for users with special permissions set
class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def suggestion_list(request):
    """
    List all suggestions for the authenticated user.
    """
    form = SuggestionDateForm(request.GET)
    if form.is_valid():
        stockPrices = StockPrice.objects.filter(date=form.cleaned_data['date'])
        return Response({'suggestions': stock_suggestions(stockPrices)})
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_root(request, format=None):
    """
    List relevant endpoints
    """
    return Response({
        'login': request.build_absolute_uri(request.get_full_path() + 'rest-auth/login/'),
        'registration': request.build_absolute_uri(request.get_full_path() + 'rest-auth/registration/'),
        'interests': reverse('interest-list', request=request, format=format),
        'stock-prices': reverse('stock-price-list', request=request, format=format),
        'stocks': reverse('stock-list', request=request, format=format),
        'suggestions': reverse('suggestion-list', request=request, format=format),
        })