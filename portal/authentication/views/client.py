from django.contrib.auth import get_user_model
from rest_framework import generics

from portal.authentication.permissions import IsPortalManager, SignUp
from portal.authentication.serializers.user import UserSerializer
from portal.authentication.services import UserAPIService
from portal.settings import CLIENT_LEVEL

User = get_user_model()


class SignUpAPIView(generics.CreateAPIView):
    """View for customers to register."""

    serializer_class = UserSerializer
    permission_classes = [SignUp]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_client(serializer)


class ClientAPIView(generics.ListAPIView):
    """View to list Clients."""

    queryset = User.objects.filter(role__level=CLIENT_LEVEL).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsPortalManager]


class ClientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Users."""

    queryset = User.objects.filter(role__level=CLIENT_LEVEL).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsPortalManager]
