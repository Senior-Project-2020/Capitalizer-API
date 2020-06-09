from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('interest/', views.InterestList.as_view()), 
    
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)