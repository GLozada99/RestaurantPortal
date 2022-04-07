from django.urls import include, path

from restaurant.views.restaurant import (
    RestaurantAPIDetailView,
    RestaurantAPIView,
)

app_name = 'restaurant'
urlpatterns = [
    path('', RestaurantAPIView.as_view(), name='restaurant-list'),
    path('<int:pk>/', RestaurantAPIDetailView.as_view(), name='restaurant-detail'),
    path(
        '<restaurant_id>/managers/',
        include(
            'authentication.urls.restaurant_manager',
            namespace='restaurant-managers'
        )
    ),
    path(
        '<restaurant_id>/dish-categories/',
        include(
            'dish.urls.dish_category',
            namespace='dish-categories'
        )
    ),
    path(
        '<restaurant_id>/branches/',
        include(
            'branch.urls.branch',
            namespace='branches'
        )
    ),
    path(
        '<restaurant_id>/ingredients/',
        include(
            'dish.urls.ingredient',
            namespace='ingredients'
        )
    ),
    path(
        '<restaurant_id>/promotions/',
        include(
            'branch.urls.promotion',
            namespace='promotions'
        )
    ),
]
