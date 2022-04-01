from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from branch.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for Branch."""
    front_picture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = Branch
        fields = ('id', 'address', 'phone_number', 'front_picture')
