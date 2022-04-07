from django.contrib.auth import get_user_model
from rest_framework import generics

from authentication.permissions import IsPortalManager, SignUp
from authentication.serializers.user import UserSerializer
from authentication.services import UserAPIService
from portal.settings import CLIENT_LEVEL

User = get_user_model()


class ClientAPIView(generics.ListCreateAPIView):
    """View to list and create Users."""

    queryset = User.objects.filter(role__level=CLIENT_LEVEL).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [SignUp | IsPortalManager]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_client(serializer)


class ClientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Users."""

    queryset = User.objects.filter(role__level=CLIENT_LEVEL).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsPortalManager]
