from django.urls import include, path

from portal.restaurant.views.restaurant import (
    RestaurantAPIDetailView,
    RestaurantAPIView,
)

app_name = 'restaurant'
urlpatterns = [
    path('', RestaurantAPIView.as_view(), name='restaurant-list'),
    path(
        '<int:pk>/',
        RestaurantAPIDetailView.as_view(),
        name='restaurant-detail',
    ),
    path(
        '<int:restaurant_id>/managers/',
        include(
            'portal.authentication.urls.restaurant_manager',
            namespace='restaurant-managers',
        ),
    ),
    path(
        '<int:restaurant_id>/dish-categories/',
        include(
            'portal.dish.urls.dish_category',
            namespace='dish-categories',
        ),
    ),
    path(
        '<int:restaurant_id>/branches/',
        include(
            'portal.branch.urls.branch',
            namespace='branches',
        ),
    ),
    path(
        '<int:restaurant_id>/ingredients/',
        include(
            'portal.dish.urls.ingredient',
            namespace='ingredients',
        ),
    ),
    path(
        '<int:restaurant_id>/promotions/',
        include(
            'portal.branch.urls.promotion',
            namespace='promotions',
        ),
    ),
]
