from secrets import token_hex

from django.contrib.auth import get_user_model
from django.db import transaction
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from portal import settings
from portal.authentication.models import Role

User = get_user_model()


class GoogleUserServices:
    @staticmethod
    def validate_token(token: str):
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request())
            if 'accounts.google.com' not in id_info['iss']:
                raise ValueError
            return id_info
        except GoogleAuthError:
            raise ValueError

    @staticmethod
    def get_user_data(data: dict):
        email = data['email']
        name = data['name']
        auth_provider = 'google'
        return {
            'email': email,
            'name': name,
            'auth_provider': auth_provider,
        }

    @staticmethod
    def validate_google_id(google_id: str):
        if google_id != settings.GOOGLE_ID:
            raise AuthenticationFailed('The token used is not from this app.')


class GeneralUserServices:
    @classmethod
    def generate_username(cls, name):
        username = "".join(name.split(' ')).lower()
        if not User.objects.filter(username=username).exists():
            return username
        else:
            random_username = username + str(token_hex(5))
            return cls.generate_username(random_username)

    @staticmethod
    def get_user_data(email: str):
        authenticated_user = User.objects.get(email=email)
        return {
            'username': authenticated_user.username,
            'email': authenticated_user.email,
            'tokens': authenticated_user.get_tokens(),
        }

    @classmethod
    @transaction.atomic
    def register_get_user(cls, email: str, name: str, auth_provider: str):
        if user := User.objects.filter(email=email).first():
            if auth_provider != user.authentication_provider:
                raise AuthenticationFailed(
                    'Email already in use with another auth_provider. Please '
                    f'login with {user.authentication_provider}')
        else:
            role = Role.objects.get(level=settings.CLIENT_LEVEL)
            user = User.objects.create_user(
                username=cls.generate_username(name),
                email=email,
                role=role,
                password=token_hex(),
                provider=auth_provider,
            )
            user.save()
        return cls.get_user_data(email)
