from django.urls import path

from restaurant.views.restaurant import (
    RestaurantAPIDetailView,
    RestaurantAPIView,
)

app_name = 'restaurant'
urlpatterns = [
    path('', RestaurantAPIView.as_view(), name='restaurant-list'),
    path('<pk>/', RestaurantAPIDetailView.as_view(), name='restaurant-detail'),
]
