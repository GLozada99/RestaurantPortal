from rest_framework import generics

from authentication.models import User
from authentication.permissions import IsPortalManager
from authentication.serializers import UserSerializer
from authentication.services import UserAPIService
from portal.settings import PORTAL_MANAGER_LEVEL


class PortalManagerAPIView(generics.ListCreateAPIView):
    """View to list and create Users."""

    queryset = User.objects.filter(
        role__level=PORTAL_MANAGER_LEVEL
    ).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsPortalManager]

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_portal_manager(serializer)


class PortalManagerAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Users."""

    queryset = User.objects.filter(
        role__level=PORTAL_MANAGER_LEVEL
    ).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsPortalManager]
