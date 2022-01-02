from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from enumfields import EnumIntegerField

from cooklist_api.common.models import UpdateCreateTimeStampedModel
from cooklist_api.recipes.enums import RecipeType, MeasureType, MealType


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        "recipes.Recipe", related_name="+", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="ingredients", on_delete=models.PROTECT
    )
    measure_type = models.CharField(
        max_length=50,
        choices=MeasureType.choices,
        default=MeasureType.G,
    )
    amount = models.FloatField()

    class Meta:
        unique_together = ["recipe", "product", "measure_type", "amount"]

    def __str__(self):
        return self.product.name


class Recipe(UpdateCreateTimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_recipes",
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.CharField(max_length=255)
    preparation_time = models.DurationField()
    servings = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes", blank=True)
    public = models.BooleanField(default=True)
    image = models.ImageField(blank=True)
    utensils = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    type = EnumIntegerField(RecipeType)

    def __str__(self):
        return self.title


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
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="scheduled_recipes",
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe, related_name="schedule", on_delete=models.PROTECT
    )
    date = models.DateField()
    meal_type = EnumIntegerField(MealType)
