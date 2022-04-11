from rest_framework import generics

from portal.authentication.permissions import IsPortalManager
from portal.restaurant.models import DeliveryType
from portal.restaurant.serializers.delivery_type import DeliveryTypeSerializer


class DeliveryTypeAPIView(generics.ListAPIView):
    """View to list DeliveryTypes."""

    queryset = DeliveryType.objects.all().order_by('id')
    serializer_class = DeliveryTypeSerializer
    permission_classes = [IsPortalManager]


class DeliveryTypeAPIDetailView(generics.RetrieveAPIView):
    """View to retrieve DeliveryTypes."""

    queryset = DeliveryType.objects.all().order_by('id')
    serializer_class = DeliveryTypeSerializer
    permission_classes = [IsPortalManager]
