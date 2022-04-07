from django.urls import path

from restaurant.views.food_type import (
    FoodTypeAPIDetailView,
    FoodTypeAPIView,
)

app_name = 'restaurant'
urlpatterns = [
    path('', FoodTypeAPIView.as_view(), name='food-type-list'),
    path(
        '<int:pk>/',
        FoodTypeAPIDetailView.as_view(),
        name='food-type-detail'
    ),
]
