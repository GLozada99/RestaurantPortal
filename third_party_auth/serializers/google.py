from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from portal import settings
from third_party_auth.services import GeneralUserServices, GoogleUserServices


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        try:
            user_data = GoogleUserServices.validate_token(token)
        except ValueError:
            raise ValidationError(
                'The token is invalid. Please login again'
            )

        if user_data.get('aud') != settings.GOOGLE_ID:
            raise AuthenticationFailed('Wrong ID')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        auth_provider = 'google'

        return GeneralUserServices.register_user(
            email=email, name=name, provider=auth_provider
        )
