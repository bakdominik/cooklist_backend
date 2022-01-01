from django.contrib import admin
from django.urls import path, include


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
