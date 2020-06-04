from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('user-info/', views.UserInfoList.as_view()),    
    path('user-info/<int:pk>', views.UserInfoDetail.as_view()),
    path('interest/', views.InterestList.as_view()), 
]

urlpatterns = format_suffix_patterns(urlpatterns)