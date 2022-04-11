from rest_framework import generics

from portal.authentication.permissions import IsPortalManager
from portal.restaurant.models import Restaurant
from portal.restaurant.serializers.restaurant import (
    CreateRestaurantSerializer, ReadRestaurantSerializer, )


class RestaurantAPIView(generics.ListCreateAPIView):
    """View to list and create Restaurants."""

    queryset = Restaurant.objects.all().order_by('id')
    permission_classes = [IsPortalManager]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateRestaurantSerializer
        return ReadRestaurantSerializer


class RestaurantAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Restaurants."""

    queryset = Restaurant.objects.all().order_by('id')
    permission_classes = [IsPortalManager]

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return CreateRestaurantSerializer
        return ReadRestaurantSerializer
