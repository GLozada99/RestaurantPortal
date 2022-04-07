from django.urls import include, path

from branch.views.branch import BranchAPIDetailView, BranchAPIView
from dish.views.dish import DishBranchAvailableAPIView

app_name = 'branch'
urlpatterns = [
    path('', BranchAPIView.as_view(), name='branch-list'),
    path(
        '<int:branch_id>/managers/',
        include(
            'authentication.urls.branch_manager',
            namespace='branch-managers',
        ),
    ),
    path(
        '<int:branch_id>/employees/',
        include(
            'authentication.urls.employee',
            namespace='employees',
        ),
    ),
    path(
        '<int:pk>/',
        BranchAPIDetailView.as_view(),
        name='branch-detail',
    ),
    path(
        '<int:branch_id>/inventory/',
        include('branch.urls.inventory', namespace='inventory'),
    ),
    path(
        '<int:branch_id>/dishes/',
        DishBranchAvailableAPIView.as_view(),
        name='available-dishes',
    ),
]
