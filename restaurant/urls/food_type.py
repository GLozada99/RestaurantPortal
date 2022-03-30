from django.urls import path

from restaurant.views.food_type import (FoodTypeAPIDetailView,
                                        FoodTypeAPIView,)

app_name = 'authentication'
urlpatterns = [
    path('', FoodTypeAPIView.as_view(), name='food-type-list'),
    path('<pk>/', FoodTypeAPIDetailView.as_view(), name='food-type-detail'),
]
