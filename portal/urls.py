from django.urls import include, path, re_path

from portal.documentation import schema_view

urlpatterns = [
    path('auth/', include('portal.authentication.urls.jwt', namespace='auth')),
    path(
        'roles/',
        include(
            'portal.authentication.urls.role', namespace='roles',
        ),
    ),
    path(
        'clients/',
        include('portal.authentication.urls.client', namespace='clients')
    ),
    path(
        'portal-managers/',
        include(
            'portal.authentication.urls.portal_manager',
            namespace='portal_managers',
        ),
    ),
    path(
        'food-types/',
        include(
            'portal.restaurant.urls.food_type',
            namespace='food_types',
        ),
    ),
    path(
        'delivery-types/',
        include(
            'portal.restaurant.urls.delivery_type',
            namespace='delivery_types',
        ),
    ),
    path(
        'restaurants/',
        include(
            'portal.restaurant.urls.restaurant',
            namespace='restaurants',
        ),
    ),
    path(
        'order-status/',
        include(
            'portal.order.urls.order_status',
            namespace='restaurants',
        ),
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        r'^$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
