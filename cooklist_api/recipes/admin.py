from django.contrib import admin

from cooklist_api.common.admin_utils import CustomModelAdmin
from cooklist_api.recipes.models import (
    Recipe,
    ScheduledRecipe,
    Ingredient,
    Product,
    RecipeStep,
)


class RecipeStepsInline(admin.StackedInline):
    model = RecipeStep
    list_display = ("title", "content")
    suit_classes = "suit-tab suit-tab-recipe-steps"
    order_by = "step_number"


class IngredientsInline(admin.StackedInline):
    model = Ingredient
    list_display = ("product__name", "measure_type", "amount")
    suit_classes = "suit-tab suit-tab-recipe-steps"


@admin.register(Recipe)
class RecipeAdmin(CustomModelAdmin):
    list_display = ("id", "owner", "title", "type", "servings", "public", "created_at")
    readonly_fields = ("id", "created_at")
    list_filter = ("type", "public", "owner")
    search_fields = (
        "id",
        "title",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )
    raw_id_fields = ("owner",)
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "id",
                    "owner",
                    "title",
                    "type",
                    "servings",
                    "preparation_time",
                    "image",
                    "public",
                    "created_at",
                ),
                "classes": (
                    "suit-tab",
                    "suit-tab-general",
                ),
            },
        ),
    )
    suit_form_tabs = (
        ("general", "General"),
        ("ingredients", "Ingredients"),
        ("steps", "Steps"),
    )
    inlines = [IngredientsInline, RecipeStepsInline]


@admin.register(ScheduledRecipe)
class ScheduledRecipeAdmin(CustomModelAdmin):
    list_display = ("id", "recipe", "date", "meal_type")
    readonly_fields = ("id",)
    list_filter = ("meal_type",)
    search_fields = ("id", "recipe__title")
    raw_id_fields = ("recipe",)
    fieldsets = (
        (
            "General",
            {
                "fields": ("id", "recipe", "date", "meal_type"),
                "classes": (
                    "suit-tab",
                    "suit-tab-general",
                ),
            },
        ),
    )
    suit_form_tabs = (("general", "General"),)


@admin.register(Product)
class ProductAdmin(CustomModelAdmin):
    list_display = ("id", "name")
    readonly_fields = ("id",)
    search_fields = ("id", "name")
    fieldsets = (
        (
            "General",
            {
                "fields": ("id", "name"),
                "classes": (
                    "suit-tab",
                    "suit-tab-general",
                ),
            },
        ),
    )
    suit_form_tabs = (("general", "General"),)
