from django.urls import include, path

from dish.views.dish_category import (
    DishCategoryAPIDetailView,
    DishCategoryAPIView,
)

app_name = 'dish-category'
urlpatterns = [
    path('', DishCategoryAPIView.as_view(), name='dish-category-list'),
    path(
        '<pk>/',
        DishCategoryAPIDetailView.as_view(),
        name='dish-category-detail'
    ),
    path(
        '<dish_category_id>/dishes/',
        include('dish.urls.dish', namespace='dishes')
    ),
]
