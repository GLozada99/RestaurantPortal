import random

from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import Role
from portal import settings

User = get_user_model()


class GoogleUserServices:
    @staticmethod
    def validate_token(token: str):
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except GoogleAuthError:
            raise ValueError


class GeneralUserServices:
    @classmethod
    def generate_username(cls, name):
        username = "".join(name.split(' ')).lower()
        if not User.objects.filter(username=username).exists():
            return username
        else:
            random_username = username + str(random.randint(0, 10000))
            return cls.generate_username(random_username)

    @staticmethod
    def get_user_data(email: str):
        authenticated_user = authenticate(
            email=email, password=settings.THIRD_PARTY_SECRET
        )
        return {
            'username': authenticated_user.username,
            'email': authenticated_user.email,
            'tokens': authenticated_user.get_tokens()
        }

    @classmethod
    @transaction.atomic
    def register_get_user(cls, email: str, name: str, provider: str):
        if user := User.objects.filter(email=email).first():
            if provider != user.authentication_provider:
                raise AuthenticationFailed(
                    'Email already in use with another provider. Please '
                    f'login with {user.authentication_provider}')
        else:
            role = Role.objects.filter(level=settings.CLIENT_LEVEL).first()
            user = {
                'username': cls.generate_username(name),
                'email': email,
                'role': role,
                'password': settings.THIRD_PARTY_SECRET,
                'provider': provider
            }
            user = User.objects.create_user(**user)
            user.save()
        return cls.get_user_data(email)
