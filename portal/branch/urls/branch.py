from django.urls import include, path

from portal.branch.views.branch import BranchAPIDetailView, BranchAPIView
from portal.dish.views.dish import (DishBranchCategoryAvailableAPIView, )

app_name = 'branch'
urlpatterns = [
    path('', BranchAPIView.as_view(), name='branch-list'),
    path(
        '<int:branch_id>/managers/',
        include(
            'portal.authentication.urls.branch_manager',
            namespace='branch-managers',
        ),
    ),
    path(
        '<int:branch_id>/employees/',
        include(
            'portal.authentication.urls.employee',
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
        include('portal.branch.urls.inventory', namespace='inventory'),
    ),
    path(
        '<int:branch_id>/categories/<int:dish_category_id>/dishes/',
        DishBranchCategoryAvailableAPIView.as_view(),
        name='available-dishes',
    ),
    path(
        '<int:branch_id>/orders/',
        include('portal.order.urls.order', namespace='orders'),
    ),
]
