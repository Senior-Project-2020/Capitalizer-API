from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('interest/', views.InterestList.as_view()), 
    path('stock-price/', views.StockPriceList.as_view()), 
    path('stock-price/<int:pk>', views.StockPriceDetail.as_view()), 
    path('stock/', views.StockList.as_view()), 
    path('stock/<int:pk>', views.StockDetail.as_view()),
    path('suggestion/', views.suggestion_list),
    
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)