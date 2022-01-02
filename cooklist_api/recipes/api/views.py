from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from cooklist_api.recipes.api.filters import RecipeFilter, ScheduledRecipeFilter
from cooklist_api.recipes.api.serializers import (
    RecipeSerializer,
    UpdateCreateRecipeSerializer,
    ScheduledRecipeSerializer,
    CreateScheduledRecipeSerializer,
)
from cooklist_api.recipes.models import Recipe, Ingredient, Product, ScheduledRecipe
from cooklist_api.recipes.permissions import RecipePermission, ScheduledRecipePermission


class RecipeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
    do_pagination = True
    permission_classes = (RecipePermission,)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return UpdateCreateRecipeSerializer
        return self.serializer_class

    def get_queryset(self):
        return (
            Recipe.objects.select_related("owner")
            .prefetch_related("steps", "ingredients")
            .filter(Q(public=True) | Q(owner=self.request.user.id))
            .order_by("-created_at")
        )

    @atomic
    def create(self, request):
        ingredients = request.data.pop("ingredients")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        self._add_ingredients(ingredients, recipe)
        headers = self.get_success_headers(serializer.data)
        created_recipe_serializer = RecipeSerializer(recipe)
        return Response(
            created_recipe_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        ingredients = request.data.pop("ingredients")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.ingredients.clear()
        self._add_ingredients(ingredients, instance)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        updated_recipe_serializer = RecipeSerializer(instance)
        return Response(
            updated_recipe_serializer.data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _add_ingredients(ingredients: list, recipe: Recipe):
        for ingredient in ingredients:
            product, _ = Product.objects.get_or_create(
                name=ingredient["product"]["name"]
            )
            ingredient, _ = Ingredient.objects.get_or_create(
                recipe=recipe,
                product=product,
                measure_type=ingredient["measure_type"],
                amount=ingredient["amount"],
            )
            recipe.ingredients.add(ingredient)


class ScheduledRecipeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (ScheduledRecipePermission,)
    filter_class = ScheduledRecipeFilter
    serializer_class = ScheduledRecipeSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "create":
            return CreateScheduledRecipeSerializer
        return self.serializer_class

    def get_queryset(self):
        return (
            ScheduledRecipe.objects.select_related("recipe")
            .filter(owner=self.request.user)
            .order_by("-date")
        )
