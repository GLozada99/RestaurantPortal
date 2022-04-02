from django.urls import path

from dish.views.ingredient import (
    IngredientAPIDetailView,
    IngredientAPIView,
)

app_name = 'dish'
urlpatterns = [
    path('', IngredientAPIView.as_view(), name='ingredient-list'),
    path(
        '<pk>/',
        IngredientAPIDetailView.as_view(),
        name='ingredient-detail'
    ),
]
