from rest_framework import serializers

from portal.authentication.serializers.user import UserSerializer
from portal.branch.serializers.branch import ShortBranchSerializer
from portal.branch.serializers.promotion import ShortPromotionSerializer
from portal.dish.serializers.dish import ShortDishSerializer
from portal.order.models import Order
from portal.order.serializers.order_dish import OrderDishSerializer
from portal.order.serializers.order_promotion import OrderPromotionSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for Dish."""
    dishes = OrderDishSerializer(many=True, required=False)
    promotions = OrderPromotionSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = (
            'id',
            'delivery_type',
            'address',
            'dishes',
            'promotions',
        )


class DetailedOrderSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish."""

    client = UserSerializer()
    status = serializers.SlugRelatedField(
        read_only=True, slug_field='name',
    )
    branch = ShortBranchSerializer()
    delivery_type = serializers.SlugRelatedField(
        read_only=True, slug_field='name',
    )
    dishes = ShortDishSerializer(many=True)
    promotions = ShortPromotionSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'client',
            'status',
            'total_cost',
            'branch',
            'address',
            'delivery_type',
            'dishes',
            'promotions',
            'created_at',
        )


class StatusOrderSerializer(serializers.ModelSerializer):
    """Serializer for Updating Dish Status."""

    class Meta:
        model = Order
        fields = ('status',)
