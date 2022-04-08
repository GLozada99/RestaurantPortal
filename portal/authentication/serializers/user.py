from rest_framework import serializers

from portal.authentication.models import User


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


class PasswordChangeSerializer(serializers.ModelSerializer):
    """Serializer for changing password"""
    previous_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'previous_password',
            'new_password',
        )
