from rest_framework import serializers

from portal.order.models import OrderStatus


class ShortOrderStatusSerializer(serializers.ModelSerializer):
    """Short Serializer for OrderStatus"""

    class Meta:
        model = OrderStatus
        fields = (
            'id',
            'name',
        )


class OrderStatusSerializer(serializers.ModelSerializer):
    """Serializer for OrderStatus"""
    previous_status = ShortOrderStatusSerializer()

    class Meta:
        model = OrderStatus
        fields = (
            'id',
            'name',
            'previous_status'
        )
