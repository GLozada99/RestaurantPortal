from rest_framework import generics

from authentication.models import Role
from authentication.permissions import IsPortalManager
from authentication.serializers import RoleSerializer


class RoleAPIView(generics.ListAPIView):
    """View to list Roles."""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = [IsPortalManager]


class RoleAPIDetailView(generics.RetrieveAPIView):
    """View to retrieve Roles."""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = [IsPortalManager]
