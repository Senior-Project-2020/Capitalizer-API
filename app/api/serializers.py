from rest_framework import serializers

from .models import PCUser, Interest, StockPrice, Stock

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'interest']

class StockPriceSerializer(serializers.ModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(many=False, queryset=Stock.objects.all())

    class Meta:
        model = StockPrice
        fields = ['id', 'stock', 'date', 'predicted_closing_price', 'opening_price', 'actual_closing_price', 'daily_high', 'daily_low', 'volume']

class StockSerializer(serializers.ModelSerializer):
    stock_prices = serializers.PrimaryKeyRelatedField(many=True, queryset=StockPrice.objects.all())

    class Meta:
        model = Stock
        fields = ['name', 'symbol', 'category', 'stock_prices']

class PCUserDetailSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(many=True, queryset=Interest.objects.all())

    class Meta:
        model = PCUser
        fields = ['id', 'username', 'email', 'interests']