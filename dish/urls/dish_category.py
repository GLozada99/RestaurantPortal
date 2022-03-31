from django.urls import path

from dish.views.dish_category import (
    DishCategoryAPIDetailView,
    DishCategoryAPIView,
)

app_name = 'dish'
urlpatterns = [
    path('', DishCategoryAPIView.as_view(), name='dish-category-list'),
    path(
        '<pk>/',
        DishCategoryAPIDetailView.as_view(),
        name='dish-category-detail'
    ),
]
