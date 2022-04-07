from django.urls import path

from authentication.views.employee import (
    EmployeeAPIDetailView, EmployeeAPIView, )

app_name = 'employee'
urlpatterns = [
    path('', EmployeeAPIView.as_view(),
         name='employee-list'),
    path(
        '<int:pk>/',
        EmployeeAPIDetailView.as_view(),
        name='employee-detail'
    ),
]
