from django.urls import path

from authentication.views.employee import (
    EmployeeAPIDetailView, EmployeeAPIView, )

app_name = 'authentication'
urlpatterns = [
    path('', EmployeeAPIView.as_view(),
         name='employee-list'),
    path(
        '<pk>/',
        EmployeeAPIDetailView.as_view(),
        name='employee-detail'
    ),
]
