from django.urls import path

from branch.views.inventory import InventoryAPIDetailView, InventoryAPIView

app_name = 'branch'
urlpatterns = [
    path('', InventoryAPIView.as_view(), name='inventory-list'),
    path(
        '<pk>/',
        InventoryAPIDetailView.as_view(),
        name='inventory-detail'
    ),
]
