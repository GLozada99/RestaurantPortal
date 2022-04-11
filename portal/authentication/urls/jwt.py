from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from portal.authentication.views.password import PasswordAPIView

app_name = 'authentication'
urlpatterns = [
    path('jwt/', TokenObtainPairView.as_view(), name='obtain-token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path(
        'google/',
        include(
            'portal.third_party_auth.urls.google',
            namespace='google',
        ),
    ),
    path(
        'change-password/',
        PasswordAPIView.as_view(),
        name='change-password',
    ),
]
