from django.urls import path

from restaurant.views.delivery_type import (
    DeliveryTypeAPIDetailView,
    DeliveryTypeAPIView,
)

app_name = 'restaurant'
urlpatterns = [
    path('', DeliveryTypeAPIView.as_view(), name='delivery-type-list'),
    path(
        '<int:pk>/',
        DeliveryTypeAPIDetailView.as_view(),
        name='delivery-type-detail',
    ),
]
