from rest_framework import serializers

from portal.authentication.models import Role


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role"""

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'level',
        )
