from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

User = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        user = User.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            return user

        return None
