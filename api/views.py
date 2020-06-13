from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Interest, StockPrice, Stock, PCUser
from .serializers import InterestSerializer, StockPriceSerializer, StockSerializer, SuggestionSerializer

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
    user = PCUser.objects.get(username=request.user)
    serializer = SuggestionSerializer(user)
    return Response(serializer.data)