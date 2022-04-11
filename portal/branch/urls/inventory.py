from django.urls import path

from portal.branch.views.inventory import (InventoryAPIDetailView,
                                           InventoryAPIView, )

app_name = 'branch'
urlpatterns = [
    path('', InventoryAPIView.as_view(), name='inventory-list'),
    path(
        '<int:pk>/',
        InventoryAPIDetailView.as_view(),
        name='inventory-detail',
    ),
]
