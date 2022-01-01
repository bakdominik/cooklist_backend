from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from enumfields import EnumIntegerField

from cooklist_api.common.models import UpdateCreateTimeStampedModel
from cooklist_api.recipes.enums import RecipeType, MeasureType, MealType


class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(UpdateCreateTimeStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="authored_recipes",
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=255)
    preparation_time = models.DurationField()
    servings = models.IntegerField()
    ingredients = models.ManyToManyField(
        Product, blank=True, through="recipes.Ingredient"
    )
    public = models.BooleanField(default=True)
    image = models.ImageField(blank=True)
    utensils = ArrayField(models.CharField(max_length=255))
    type = EnumIntegerField(RecipeType)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="ingredients", on_delete=models.CASCADE
    )
    measure_type = models.CharField(
        max_length=50,
        choices=MeasureType.choices,
        default=MeasureType.G,
    )
    amount = models.FloatField()

    def __str__(self):
        return self.product.name


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)
    step_number = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        unique_together = ["recipe", "step_number"]

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class ScheduledRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="schedule", on_delete=models.CASCADE
    )
    date_scheduled = models.DateField()
    meal_type = EnumIntegerField(MealType)
