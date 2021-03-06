from django.db import models
from django.contrib.auth.models import AbstractUser

class Interest(models.Model):
    interest = models.CharField(max_length=100)

    def __str__(self):
        return self.interest

    class Meta:
        ordering = ['interest']

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100, primary_key=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.symbol

    class Meta:
        ordering = ['name']

class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, related_name='stock_prices', on_delete=models.CASCADE)
    date = models.DateField()
    predicted_closing_price = models.DecimalField(max_digits=12, decimal_places=2)
    opening_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    actual_closing_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    daily_high = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    daily_low = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

class PCUser(AbstractUser):
    # Get interests from the Interest table
    interests = models.ManyToManyField(Interest)
