from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions, authentication

urlpatterns = [
    path("admin/", admin.site.urls),
    # COOKLIST API APPS URLS
    path(
        "api/v1/recipes/",
        include(
            ("cooklist_api.recipes.urls", "cooklist_api.recipes"),
            namespace="cooklist-api-v1-recipes",
        ),
    ),
]
# SWAGGER
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Cooklist API", default_version="1.0", description="Docs for Cooklist API"
    ),
    url=None,
    public=True,
    permission_classes=(permissions.IsAdminUser,),
    authentication_classes=(authentication.SessionAuthentication,),
)

urlpatterns += [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
