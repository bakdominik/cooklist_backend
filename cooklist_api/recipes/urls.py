from rest_framework.routers import DefaultRouter

from cooklist_api.recipes.api.views import RecipeViewSet, ScheduledRecipeViewSet

router = DefaultRouter()

router.register(r"recipes", RecipeViewSet, "Recipe")
router.register(r"scheduled-recipes", ScheduledRecipeViewSet, "ScheduledRecipe")

urlpatterns = router.urls
