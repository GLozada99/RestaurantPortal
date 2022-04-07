from django.urls import path

from portal.dish.views.dish import (
    DishAPIDetailView,
    DishAPIView,
)

app_name = 'dish'
urlpatterns = [
    path('', DishAPIView.as_view(), name='dish-list'),
    path('<int:pk>/', DishAPIDetailView.as_view(), name='dish-detail'),
]
