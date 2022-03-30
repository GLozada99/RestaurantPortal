from rest_framework import generics

from authentication.models import Role, User
from authentication.serializers import RoleSerializer, UserSerializer
from authentication.services import UserAPIService
from portal.settings import CLIENT_LEVEL, PORTAL_MANAGER_LEVEL


class RoleAPIView(generics.ListAPIView):
    """View to list Roles."""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer


class RoleAPIDetailView(generics.RetrieveAPIView):
    """View to retrieve Roles."""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer


class ClientAPIView(generics.ListCreateAPIView):
    """View to list and create Users."""

    queryset = User.objects.filter(role__level=CLIENT_LEVEL).order_by('id')
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_client(serializer)


class ClientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Users."""

    queryset = User.objects.filter(role__level=CLIENT_LEVEL).order_by('id')
    serializer_class = UserSerializer


class PortalManagerAPIView(generics.ListCreateAPIView):
    """View to list and create Users."""

    queryset = User.objects.filter(role__level=PORTAL_MANAGER_LEVEL).order_by(
        'id')
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_portal_manager(serializer)


class PortalManagerAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Users."""

    queryset = User.objects.filter(role__level=PORTAL_MANAGER_LEVEL).order_by(
        'id')
    serializer_class = UserSerializer
