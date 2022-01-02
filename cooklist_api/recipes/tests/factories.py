from datetime import timedelta

import factory
from django.utils.timezone import now
from factory import SubFactory
from factory.django import DjangoModelFactory

from cooklist_api.recipes.enums import RecipeType, MealType
from cooklist_api.recipes.models import Recipe, Ingredient, Product, ScheduledRecipe


class RecipeFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Test Recipe {n}")
    preparation_time = timedelta(minutes=40)
    servings = 4
    utensils = ["utensil 1", "utensil 2"]
    type = RecipeType.MAIN_COURSE

    class Meta:
        model = Recipe


class ScheduledRecipeFactory(DjangoModelFactory):
    recipe = SubFactory(RecipeFactory)
    date = now()
    meal_type = MealType.BREAKFAST

    class Meta:
        model = ScheduledRecipe


class ProductFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Test Product {n}")

    class Meta:
        model = Product


class IngredientFactory(DjangoModelFactory):
    recipe = SubFactory(RecipeFactory)
    product = SubFactory(ProductFactory)
    amount = 250

    class Meta:
        model = Ingredient
