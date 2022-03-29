from django.urls import path

from authentication.views import UserAPIDetailView, UserAPIView

app_name = 'authentication'
urlpatterns = [
    path('', UserAPIView.as_view(), name='user-list'),
    path('<pk>/', UserAPIDetailView.as_view(), name='user-detail'),
]
