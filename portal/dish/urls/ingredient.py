from django.urls import path

from portal.dish.views.ingredient import (
    IngredientAPIDetailView,
    IngredientAPIView,
)

app_name = 'ingredient'
urlpatterns = [
    path('', IngredientAPIView.as_view(), name='ingredient-list'),
    path(
        '<int:pk>/',
        IngredientAPIDetailView.as_view(),
        name='ingredient-detail',
    ),
]
