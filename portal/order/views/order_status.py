from rest_framework import generics

from portal.order.models import OrderStatus
from portal.order.serializers.order_status import OrderStatusSerializer


class OrderStatusAPIView(generics.ListAPIView):
    """View to list OrderStatus."""

    queryset = OrderStatus.objects.all().order_by('id')
    serializer_class = OrderStatusSerializer


class OrderStatusAPIDetailView(generics.RetrieveAPIView):
    """View to retrieve OrderStatus."""

    queryset = OrderStatus.objects.all().order_by('id')
    serializer_class = OrderStatusSerializer
