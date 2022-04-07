from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

app_name = 'authentication'
urlpatterns = [
    path('jwt/', TokenObtainPairView.as_view(), name='obtain-token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path(
        'google/',
        include(
            'third_party_auth.urls.google',
            namespace='google',
        ),
    ),
]
