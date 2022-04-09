from rest_framework import generics

from portal.authentication.serializers.user import (PasswordChangeSerializer,
                                                    UserEmailSerializer,
                                                    )
from portal.authentication.services import UserAPIService


class PasswordAPIView(generics.GenericAPIView):
    """View to change User password."""
    serializer_class = PasswordChangeSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserEmailSerializer
        return PasswordChangeSerializer

    def put(self, request, *args, **kwargs):
        """Endpoint for changing password given email and token."""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.change_password(serializer)

    def post(self, request, *args, **kwargs):
        """Endpoint for asking for password reset token with email"""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.set_password_change_token(serializer)
