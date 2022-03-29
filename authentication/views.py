from rest_framework import generics

from authentication.models import Role, User
from authentication.serializers import RoleSerializer, UserSerializer


class RoleAPIView(generics.ListAPIView):
    """View to list Roles."""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer


class RoleAPIDetailView(generics.RetrieveAPIView):
    """View to retrieve Roles."""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer


class UserAPIView(generics.ListCreateAPIView):
    """View to list and create Users."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class UserAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Users."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
