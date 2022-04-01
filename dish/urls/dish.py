from django.urls import path

from dish.views.dish import (
    DishAPIDetailView,
    DishAPIView,
)

app_name = 'dish'
urlpatterns = [
    path('', DishAPIView.as_view(), name='dish-list'),
    path('<pk>/', DishAPIDetailView.as_view(), name='dish-detail'),
]
