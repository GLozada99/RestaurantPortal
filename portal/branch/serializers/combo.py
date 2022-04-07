from rest_framework import serializers

from portal.branch.models import Combo
from portal.dish.serializers.dish import ShortDishSerializer
from portal.validators import Validators


class ComboSerializer(serializers.ModelSerializer):
    """Serializer for Combo."""

    class Meta:
        model = Combo
        fields = (
            'dish',
            'quantity',
        )

    def validate_quantity(self, value):
        return Validators.validate_greater_than_zero(value)


class DetailedComboSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Combo."""

    dish = ShortDishSerializer()

    class Meta:
        model = Combo
        fields = (
            'dish',
            'quantity',
        )
