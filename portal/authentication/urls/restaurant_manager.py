from django.urls import path

from portal.authentication.views.restaurant_manager import (
    RestaurantManagerAPIDetailView,
    RestaurantManagerAPIView,
)

app_name = 'authentication'
urlpatterns = [
    path('', RestaurantManagerAPIView.as_view(),
         name='restaurant-manager-list'),
    path(
        '<int:pk>/',
        RestaurantManagerAPIDetailView.as_view(),
        name='restaurant-manager-detail',
    ),
]
