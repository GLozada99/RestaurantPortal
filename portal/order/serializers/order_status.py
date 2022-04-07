from rest_framework import serializers

from portal.order.models import OrderStatus


class OrderStatusSerializer(serializers.ModelSerializer):
    """Serializer for OrderStatus"""

    class Meta:
        model = OrderStatus
        fields = (
            'id',
            'name',
        )
