from django.contrib.auth.models import User
from django_filters import NumberFilter
from rest_framework_filters import RelatedFilter, FilterSet

from cooklist_api.common.api.filters import NumberInFilter
from cooklist_api.recipes.models import Recipe, Ingredient, Product, ScheduledRecipe
from cooklist_api.users.api.filters import UserFilter


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {"id": ["exact", "in"], "name": ["exact", "in"]}


class IngredientFilter(FilterSet):
    product = RelatedFilter(filterset=ProductFilter, queryset=Product.objects.all())

    class Meta:
        model = Ingredient
        fields = {"id": ["exact", "in"]}


class RecipeFilter(FilterSet):
    owner = RelatedFilter(filterset=UserFilter, queryset=User.objects.all())
    ingredients = RelatedFilter(
        filterset=IngredientFilter, queryset=Ingredient.objects.all()
    )
    type = NumberFilter()
    type__in = NumberInFilter(lookup_expr="in", field_name="type")

    class Meta:
        model = Recipe
        fields = {
            "id": ["exact", "in"],
            "title": ["exact", "in"],
            "preparation_time": ["exact", "in", "gt", "gte", "lt", "lte"],
            "servings": ["exact", "in", "gt", "gte", "lt", "lte"],
        }


class ScheduledRecipeFilter(FilterSet):
    owner = RelatedFilter(filterset=UserFilter, queryset=User.objects.all())
    recipe = RelatedFilter(filterset=RecipeFilter, queryset=Recipe.objects.all())

    class Meta:
        model = ScheduledRecipe
        fields = {
            "date": ["exact", "in", "gt", "gte", "lt", "lte"],
            "meal_type": ["exact", "in"],
        }
