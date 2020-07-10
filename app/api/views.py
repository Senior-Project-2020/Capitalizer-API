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

    def get_queryset(self):
        queryset = StockPrice.objects.all()
        stock = self.request.query_params.get('recent', None)

        if stock is not None:
            if stock == 'all':
                # Gets a list of dates for all stock prices
                all_dates = list(StockPrice.objects.values('date').distinct().order_by('-date'))

                # Get a list of the five most recent dates for stock prices
                recent_dates = []
                for i in range(min(len(all_dates), 5)):
                    recent_dates.append(all_dates[i]['date'])

                # Gets the stock prices for all stocks on the five most recent price dates.
                # Orders them by stock, ascending, and then date, descending. Prices from the same stock are "grouped" together.
                queryset = StockPrice.objects.filter(date__in=recent_dates).order_by('stock__symbol', '-date')

            else:
                # Order by date, newest to oldest
                queryset = StockPrice.objects.order_by('-date')
                queryset = queryset.filter(stock=stock)[:5]

        return queryset

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