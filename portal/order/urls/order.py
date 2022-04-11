from django.urls import path

from portal.order.views.order import (
    OrderAPIView,
    OrderAPIDetailView,
)

app_name = 'order'
urlpatterns = [
    path('', OrderAPIView.as_view(), name='order-list'),
    path('<int:pk>/', OrderAPIDetailView.as_view(), name='order-detail'),
]
