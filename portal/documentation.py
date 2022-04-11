from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Restaurant portal API",
      default_version='1.0.0',
      description="API for restaurants",
      terms_of_service="https://www.google.com/policies/terms/",
   ),
   public=True,
)
