from rest_framework import generics

from authentication.permissions import IsPortalManager
from restaurant.models import Restaurant
from restaurant.serializers.restaurant import (
    DetailedRestaurantSerializer,
    RestaurantSerializer,
)


class RestaurantAPIView(generics.ListCreateAPIView):
    """View to list and create Restaurants."""

    queryset = Restaurant.objects.all().order_by('id')
    permission_classes = [IsPortalManager]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RestaurantSerializer
        return DetailedRestaurantSerializer


class RestaurantAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Restaurants."""

    queryset = Restaurant.objects.all().order_by('id')
    permission_classes = [IsPortalManager]

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return RestaurantSerializer
        return DetailedRestaurantSerializer
