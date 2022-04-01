from django.urls import include, path

from restaurant.views.restaurant import (
    RestaurantAPIDetailView,
    RestaurantAPIView,
)

app_name = 'restaurant'
urlpatterns = [
    path('', RestaurantAPIView.as_view(), name='restaurant-list'),
    path('<pk>/', RestaurantAPIDetailView.as_view(), name='restaurant-detail'),
    path(
        '<restaurant_pk>/dish-categories/',
        path(
            'dish-categories/',
            include(
                'dish.urls.dish_category',
                namespace='dish-categories'
            )
        ),
    )
]
