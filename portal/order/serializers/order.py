from rest_framework import serializers

from authentication.serializers.user import UserSerializer
from branch.serializers.branch import ShortBranchSerializer
from portal.order.models import Order
from portal.order.serializers.order_dish import OrderDishSerializer
from portal.order.serializers.order_promotion import OrderPromotionSerializer
from portal.order.serializers.order_status import OrderStatusSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for Dish."""
    dishes = OrderDishSerializer(many=True)
    promotions = OrderPromotionSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'address'
            'dishes',
            'promotions',
        )


class DetailedOrderSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish."""
    client = UserSerializer()
    status = OrderStatusSerializer()
    branch = ShortBranchSerializer()

    class Meta:
        model = Order
        fields = (
            'client',
            'status',
            'branch',
            'address'
            'dishes',
            'promotions',
        )
