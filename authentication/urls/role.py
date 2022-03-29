from django.urls import path

from authentication.views import RoleAPIDetailView, RoleAPIView

app_name = 'authentication'
urlpatterns = [
    path('', RoleAPIView.as_view(), name='role-list'),
    path('<pk>/', RoleAPIDetailView.as_view(), name='role-detail'),
]
