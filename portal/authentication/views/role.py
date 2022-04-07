from rest_framework import generics

from portal.authentication.models import Role
from portal.authentication.permissions import IsPortalManager
from portal.authentication.serializers.role import RoleSerializer


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
