from rest_framework import generics

from authentication.models import Role, User
from authentication.serializers import RoleSerializer, UserSerializer
from authentication.services import UserAPIService


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

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create(serializer)


class UserAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Users."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
