from rest_framework import generics

from authentication.permissions import IsRestaurantManager, ReadOnly
from branch.models import Promotion
from branch.serializers.promotion import (
    DetailedPromotionSerializer,
    PromotionSerializer,
)
from branch.services.promotion import PromotionAPIService


class PromotionAPIView(generics.ListCreateAPIView):
    """View to list and create Promotion."""

    permission_classes = [IsRestaurantManager | ReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PromotionSerializer
        return DetailedPromotionSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Promotion.objects.filter(restaurant_id=restaurant_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return PromotionAPIService.create(
            serializer, self.kwargs.get('restaurant_id'),
        )


class PromotionAPIDetailView(generics.RetrieveDestroyAPIView):
    """View to retrieve, update and delete Promotion."""

    permission_classes = [IsRestaurantManager | ReadOnly]

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return PromotionSerializer
        return DetailedPromotionSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Promotion.objects.filter(restaurant_id=restaurant_id)
