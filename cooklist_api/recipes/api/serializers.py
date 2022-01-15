from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from cooklist_api.recipes.models import (
    Recipe,
    Ingredient,
    Product,
    ScheduledRecipe,
    FavouriteRecipe,
)
from cooklist_api.users.api.serializers import SlimUserSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Ingredient
        exclude = ["recipe"]


class RecipeSerializer(serializers.ModelSerializer):
    owner = SlimUserSerializer()
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "owner",
            "title",
            "preparation_time",
            "servings",
            "ingredients",
            "public",
            "image",
            "utensils",
            "type",
            "created_at",
            "updated_at",
        )


class UpdateCreateRecipeSerializer(serializers.ModelSerializer):
    type = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            "owner",
            "title",
            "preparation_time",
            "servings",
            "public",
            "image",
            "utensils",
            "type",
            "created_at",
            "updated_at",
        )


class SlimRecipeSerializer(serializers.ModelSerializer):
    owner = SlimUserSerializer()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "owner",
            "title",
            "preparation_time",
            "servings",
            "image",
        )


class ScheduledRecipeSerializer(serializers.ModelSerializer):
    meal_type = serializers.IntegerField()
    recipe = SlimRecipeSerializer()

    class Meta:
        model = ScheduledRecipe
        fields = ("id", "meal_type", "recipe", "date")


class CreateScheduledRecipeSerializer(serializers.ModelSerializer):
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    meal_type = serializers.IntegerField()

    class Meta:
        model = ScheduledRecipe
        fields = ("owner", "recipe", "meal_type", "date")


class FavouriteRecipeSerializer(serializers.ModelSerializer):
    recipe = SlimRecipeSerializer()

    class Meta:
        model = FavouriteRecipe
        fields = ("id", "recipe")


class CreateFavouriteRecipeSerializer(serializers.ModelSerializer):
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = FavouriteRecipe
        fields = ("recipe", "owner")
