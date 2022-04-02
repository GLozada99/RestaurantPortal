from rest_framework import generics

from restaurant.models import FoodType
from restaurant.serializers.food_type import FoodTypeSerializer


class FoodTypeAPIView(generics.ListAPIView):
    """View to list FoodTypes."""

    queryset = FoodType.objects.all().order_by('id')
    serializer_class = FoodTypeSerializer
    # permission_classes = [IsPortalManager]


class FoodTypeAPIDetailView(generics.RetrieveAPIView):
    """View to retrieve FoodTypes."""

    queryset = FoodType.objects.all().order_by('id')
    serializer_class = FoodTypeSerializer
    # permission_classes = [IsPortalManager]
