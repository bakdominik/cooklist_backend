from rest_framework.routers import DefaultRouter

from cooklist_api.recipes.api.views import (
    RecipeViewSet,
    ScheduledRecipeViewSet,
    FavouriteRecipeViewSet,
)

router = DefaultRouter()

router.register(r"recipes", RecipeViewSet, "Recipe")
router.register(r"scheduled-recipes", ScheduledRecipeViewSet, "ScheduledRecipe")
router.register(r"favourite-recipes", FavouriteRecipeViewSet, "FavouriteRecipe")

urlpatterns = router.urls
