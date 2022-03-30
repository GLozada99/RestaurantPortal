from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

app_name = 'authentication'
urlpatterns = [
     path('', TokenObtainPairView.as_view(), name='obtain-token'),
     path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]
