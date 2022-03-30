from rest_framework import serializers

from authentication.models import Role, User


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role"""

    class Meta:
        model = Role
        fields = ('id', 'name', 'level')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
        )
