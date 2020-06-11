from django.contrib import admin

from .models import Interest, PCUser, StockPrice, Stock

admin.site.register(Interest)
admin.site.register(StockPrice)
admin.site.register(Stock)
admin.site.register(PCUser)