from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant portal API",
        default_version='1.0.0',
        description="API for restaurants",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
)
