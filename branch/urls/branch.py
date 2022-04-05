from django.urls import include, path

from branch.views.branch import BranchAPIDetailView, BranchAPIView

app_name = 'branch'
urlpatterns = [
    path('', BranchAPIView.as_view(), name='branch-list'),
    path(
        '<branch_id>/managers/',
        include(
            'authentication.urls.branch_manager',
            namespace='branch-managers'
        )
    ),
    path(
        '<branch_id>/employees/',
        include(
            'authentication.urls.employee',
            namespace='employees'
        )
    ),
    path(
        '<pk>/',
        BranchAPIDetailView.as_view(),
        name='branch-detail'
    ),
    path(
        '<branch_id>/inventory/',
        include('branch.urls.inventory', namespace='inventory')
    ),
]
