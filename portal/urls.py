from django.urls import path, include, re_path

from portal.documentation import schema_view

urlpatterns = [
    path('auth/', include('authentication.urls.jwt', namespace='auth')),
    path('roles/', include('authentication.urls.role', namespace='roles')),
    path(
        'clients/',
        include('authentication.urls.client', namespace='clients')
    ),
    path(
        'portal-managers/',
        include(
            'authentication.urls.portal_manager',
            namespace='portal_managers'
        )
    ),
    path(
        'food-types/',
        include(
            'restaurant.urls.food_type',
            namespace='food_types'
        )
    ),
    path(
        'delivery-types/',
        include(
            'restaurant.urls.delivery_type',
            namespace='delivery_types'
        )
    ),
    path(
        'restaurants/',
        include(
            'restaurant.urls.restaurant',
            namespace='restaurants'
        )
    ),
    path(
        'ingredients/',
        include(
            'dish.urls.ingredient',
            namespace='ingredients'
        )
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(
            cache_timeout=0
        ), name='schema-json'
    ),
    re_path(
        r'^$',
        schema_view.with_ui(
            'swagger', cache_timeout=0
        ), name='schema-swagger-ui'
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui(
            'redoc', cache_timeout=0
        ), name='schema-redoc'
    ),
]
