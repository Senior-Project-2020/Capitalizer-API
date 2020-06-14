from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.api_root),
    path('interest/', 
         views.InterestList.as_view(), 
         name='interest-list'), 
    path('stock-price/', 
         views.StockPriceList.as_view(), 
         name='stock-price-list'), 
    path('stock-price/<int:pk>', 
         views.StockPriceDetail.as_view(), 
         name='stock-price-detail'), 
    path('stock/', 
         views.StockList.as_view(), 
         name='stock-list'), 
    path('stock/<int:pk>', 
         views.StockDetail.as_view(), 
         name='stock-detail'),
    path('suggestion/', 
         views.suggestion_list, 
         name='suggestion-list'),
    
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)