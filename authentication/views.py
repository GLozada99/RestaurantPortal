from rest_framework import generics

from authentication.models import Role, User
from authentication.serializers import RoleSerializer, UserSerializer


class RoleAPIView(generics.ListCreateAPIView):
    """View to list and create Roles"""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer


class RoleAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Roles"""

    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
