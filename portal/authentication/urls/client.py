from django.urls import path

from portal.authentication.views.client import (ClientAPIDetailView,
                                                ClientAPIView, )

app_name = 'authentication'
urlpatterns = [
    path('', ClientAPIView.as_view(), name='client-list'),
    path('<int:pk>/', ClientAPIDetailView.as_view(), name='client-detail'),
]
