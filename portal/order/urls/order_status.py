from django.urls import path

from portal.order.views.order_status import (
    OrderStatusAPIView,
    OrderStatusAPIDetailView,
)

app_name = 'order'
urlpatterns = [
    path('', OrderStatusAPIView.as_view(), name='order-status-list'),
    path(
        '<int:pk>/',
        OrderStatusAPIDetailView.as_view(),
        name='order-status-detail',
    ),
]
