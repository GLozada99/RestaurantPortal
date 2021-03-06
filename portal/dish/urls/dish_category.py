from django.urls import include, path

from portal.dish.views.dish_category import (
    DishCategoryAPIDetailView,
    DishCategoryAPIView,
)

app_name = 'dish-category'
urlpatterns = [
    path('', DishCategoryAPIView.as_view(), name='dish-category-list'),
    path(
        '<int:pk>/',
        DishCategoryAPIDetailView.as_view(),
        name='dish-category-detail',
    ),
    path(
        '<int:dish_category_id>/dishes/',
        include('portal.dish.urls.dish', namespace='dishes'),
    ),
]
