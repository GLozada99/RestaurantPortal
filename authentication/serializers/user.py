from rest_framework import serializers

from authentication.models import User


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
