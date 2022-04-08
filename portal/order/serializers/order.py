from rest_framework import serializers

from portal.authentication.serializers.user import UserSerializer
from portal.branch.serializers.branch import ShortBranchSerializer
from portal.order.models import Order
from portal.order.serializers.order_dish import OrderDishSerializer
from portal.order.serializers.order_promotion import OrderPromotionSerializer
from portal.order.serializers.order_status import OrderStatusSerializer
from portal.restaurant.serializers.delivery_type import DeliveryTypeSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for Dish."""
    dishes = OrderDishSerializer(many=True, required=False)
    promotions = OrderPromotionSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = (
            'delivery_type',
            'address',
            'dishes',
            'promotions',
        )


class DetailedOrderSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish."""
    client = UserSerializer()
    status = OrderStatusSerializer()
    branch = ShortBranchSerializer()
    delivery_type = DeliveryTypeSerializer()

    class Meta:
        model = Order
        fields = (
            'client',
            'delivery_type',
            'status',
            'branch',
            'address'
            'dishes',
            'promotions',
        )


class StatusOrderSerializer(serializers.ModelSerializer):
    """Serializer for Updating Dish Status."""

    class Meta:
        model = Order
        fields = ('status',)
