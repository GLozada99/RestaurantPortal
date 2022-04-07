from django.urls import path

from authentication.views.portal_manager import (PortalManagerAPIDetailView,
                                                 PortalManagerAPIView, )

app_name = 'portal_manager'
urlpatterns = [
    path('', PortalManagerAPIView.as_view(), name='portal-manager-list'),
    path(
        '<int:pk>/',
        PortalManagerAPIDetailView.as_view(),
        name='portal-manager-detail',
    ),
]
