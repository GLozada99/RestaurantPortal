from django.urls import path

from authentication.views import (PortalManagerAPIDetailView,
                                  PortalManagerAPIView,)

app_name = 'authentication'
urlpatterns = [
    path('', PortalManagerAPIView.as_view(), name='portal-manager-list'),
    path(
        '<pk>/',
        PortalManagerAPIDetailView.as_view(),
        name='portal-manager-detail'
    ),
]
