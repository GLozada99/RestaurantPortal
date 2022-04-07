from rest_framework import serializers

from order.models import OrderDish
from portal.validators import Validators


class OrderDishSerializer(serializers.ModelSerializer):
    """Serializer for OrderDish."""

    class Meta:
        model = OrderDish
        fields = (
            'order',
            'dish',
            'quantity',
        )

    def validate_quantity(self, value):
        return Validators.validate_greater_than_zero(value)
