from rest_framework import serializers

from portal.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User"""

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )


class PasswordChangeSerializer(serializers.ModelSerializer):
    """Serializer for changing password"""
    change_password_token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'change_password_token',
            'new_password',
        )


class UserEmailSerializer(serializers.ModelSerializer):
    """Serializer for User Email"""

    class Meta:
        model = User
        fields = (
            'email',
        )
