from rest_framework import generics

from portal.authentication.permissions import IsPortalManager
from portal.restaurant.models import FoodType
from portal.restaurant.serializers.food_type import FoodTypeSerializer


class FoodTypeAPIView(generics.ListAPIView):
    """View to list FoodTypes."""

    queryset = FoodType.objects.all().order_by('id')
    serializer_class = FoodTypeSerializer
    permission_classes = [IsPortalManager]


class FoodTypeAPIDetailView(generics.RetrieveAPIView):
    """View to retrieve FoodTypes."""

    queryset = FoodType.objects.all().order_by('id')
    serializer_class = FoodTypeSerializer
    permission_classes = [IsPortalManager]
