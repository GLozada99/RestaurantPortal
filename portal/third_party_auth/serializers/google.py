from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from portal.third_party_auth.services import (GoogleUserServices, )


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        try:
            user_data = GoogleUserServices.validate_token(token)
        except ValueError as e:
            raise ValidationError(
                'The token is invalid. Please login again'
            ) from e
        return user_data
