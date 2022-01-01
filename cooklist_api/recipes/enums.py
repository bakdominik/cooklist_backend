from enum import IntEnum

from django.db import models
from django.utils.translation import gettext_lazy as _


class RecipeType(IntEnum):
    MAIN_COURSE = 1
    SOUP = 2
    SALAD = 3
    DRINK = 4
    PREPARATION = 5
    BREAKFAST = 6
    FAST_FOOD = 7
    SNACK = 8
    DESSERT = 9
    CAKE = 10
    COOKIES = 11


class MeasureType(models.TextChoices):
    G = "G", _("g")
    ML = "ML", _("ml")
    PCS = "PCS", _("pcs")
    GLASS = "GLASS", _("glass")
    SPOON = "SPOON", _("spoon")
    TEASPOON = "TEASPOON", _("teaspoon")


class MealType(IntEnum):
    BREAKFAST = 1
    SNACK = 2
    LUNCH = 3
    TEA = 4
    DINNER = 5
