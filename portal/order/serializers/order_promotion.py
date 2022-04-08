from rest_framework import serializers

from portal.order.models import OrderPromotion
from portal.validators import Validators


class OrderPromotionSerializer(serializers.ModelSerializer):
    """Serializer for OrderPromotion."""

    class Meta:
        model = OrderPromotion
        fields = (
            'promotion',
            'quantity',
        )

    def validate_quantity(self, value):
        return Validators.validate_greater_than_zero(value)
