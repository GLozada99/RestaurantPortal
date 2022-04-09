from rest_framework import generics, status
from rest_framework.response import Response

from portal.authentication.permissions import IsRestaurantManager, ReadOnly
from portal.branch.models import Promotion
from portal.branch.serializers.promotion import DetailedPromotionSerializer
from portal.branch.handlers.promotion import PromotionAPIHandler


class PromotionAPIView(generics.ListCreateAPIView):
    """View to list and create Promotion."""

    serializer_class = DetailedPromotionSerializer
    permission_classes = [IsRestaurantManager | ReadOnly]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Promotion.objects.filter(restaurant_id=restaurant_id)

    def post(self, request, *args, **kwargs):
        data = PromotionAPIHandler.handle(request, kwargs.get('restaurant_id'))
        return Response(data, status=status.HTTP_201_CREATED)


class PromotionAPIDetailView(generics.RetrieveDestroyAPIView):
    """View to retrieve, update and delete Promotion."""

    serializer_class = DetailedPromotionSerializer
    permission_classes = [IsRestaurantManager | ReadOnly]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Promotion.objects.filter(restaurant_id=restaurant_id)
