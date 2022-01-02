from datetime import timedelta

from django.urls import reverse
from django.utils.timezone import now
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from cooklist_api.common.testing.base_test_classes import BaseTestCase
from cooklist_api.recipes.enums import MeasureType, MealType
from cooklist_api.recipes.models import Product
from cooklist_api.recipes.tests.factories import (
    RecipeFactory,
    IngredientFactory,
    ProductFactory,
    ScheduledRecipeFactory,
)
from cooklist_api.users.tests.factories import UserFactory


class TestRecipeApi(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.recipe = RecipeFactory(owner=self.user)
        self.product = ProductFactory()
        self.recipe.ingredients.add(
            IngredientFactory(product=self.product, recipe=self.recipe)
        )
        self.recipe.save()

    def test_list_authenticated(self):
        RecipeFactory(owner=self.user, public=False)
        RecipeFactory(owner=UserFactory(), public=False)

        response = self._get(
            reverse(
                "cooklist-api-v1-recipes:Recipe-list",
            ),
            user=self.user,
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        data = response.json()
        self.assertEqual(2, data["count"])
        recipe = data["results"][-1]
        self.assertEqual(self.user.first_name, recipe["owner"]["first_name"])
        self.assertEqual(1, len(recipe["ingredients"]))

    def test_list_with_filter(self):
        RecipeFactory(owner=UserFactory(), public=True)
        response = self._get(
            reverse(
                "cooklist-api-v1-recipes:Recipe-list",
            )
            + f"?owner__first_name={self.user.first_name}",
            user=self.user,
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        data = response.json()
        self.assertEqual(1, data["count"])

    def test_list_not_authenticated(self):
        RecipeFactory(owner=self.user, public=False)
        RecipeFactory(owner=UserFactory(), public=False)

        response = self._get(
            reverse(
                "cooklist-api-v1-recipes:Recipe-list",
            ),
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        data = response.json()
        self.assertEqual(1, data["count"])

    def test_retrieve(self):
        response = self._get(
            reverse("cooklist-api-v1-recipes:Recipe-detail", args=[self.recipe.id]),
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        data = response.json()
        self.assertEqual(self.user.first_name, data["owner"]["first_name"])
        self.assertEqual(self.recipe.title, data["title"])
        self.assertEqual(
            "{:0>8}".format(str(self.recipe.preparation_time)), data["preparation_time"]
        )
        self.assertEqual(self.recipe.servings, data["servings"])
        self.assertEqual(
            len(list(self.recipe.ingredients.all())), len(data["ingredients"])
        )
        ingredient = self.recipe.ingredients.get()
        self.assertEqual(ingredient.id, data["ingredients"][0]["id"])
        self.assertEqual(
            ingredient.product.id,
            data["ingredients"][0]["product"]["id"],
        )
        self.assertEqual(
            ingredient.product.name,
            data["ingredients"][0]["product"]["name"],
        )
        self.assertEqual(
            ingredient.measure_type,
            data["ingredients"][0]["measure_type"],
        )
        self.assertEqual(ingredient.amount, data["ingredients"][0]["amount"])
        self.assertEqual(self.recipe.public, data["public"])
        self.assertEqual(None, data["image"])
        self.assertEqual(self.recipe.utensils, data["utensils"])
        self.assertEqual(self.recipe.type, data["type"])

    def test_create(self):
        payload = {
            "owner": self.user.id,
            "title": "Test create recipe",
            "preparation_time": str(timedelta(minutes=20)),
            "servings": 4,
            "ingredients": [
                {
                    "product": {"name": "Test product"},
                    "measure_type": MeasureType.G,
                    "amount": 200.5,
                }
            ],
            "utensils": ["Test utensil 1", "Test utensil 2"],
            "type": 2,
        }
        response = self._post(
            reverse("cooklist-api-v1-recipes:Recipe-list"), data=payload
        )
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        data = response.json()
        self.assertEqual(self.user.first_name, data["owner"]["first_name"])
        self.assertEqual(payload["title"], data["title"])
        self.assertEqual(
            "{:0>8}".format(payload["preparation_time"]), data["preparation_time"]
        )
        self.assertEqual(
            payload["ingredients"][0]["product"]["name"].lower(),
            data["ingredients"][0]["product"]["name"],
        )
        self.assertEqual(
            payload["ingredients"][0]["measure_type"],
            data["ingredients"][0]["measure_type"],
        )
        self.assertEqual(
            payload["ingredients"][0]["amount"],
            data["ingredients"][0]["amount"],
        )
        self.assertEqual(payload["utensils"], data["utensils"])
        self.assertEqual(payload["type"], data["type"])

    def test_create_with_existing_product(self):
        product_count = Product.objects.all().count()
        payload = {
            "owner": self.user.id,
            "title": "Test create recipe",
            "preparation_time": str(timedelta(minutes=20)),
            "servings": 4,
            "ingredients": [
                {
                    "product": {"name": self.product.name},
                    "measure_type": MeasureType.G,
                    "amount": 200.5,
                }
            ],
            "utensils": ["Test utensil 1", "Test utensil 2"],
            "type": 2,
        }
        response = self._post(
            reverse("cooklist-api-v1-recipes:Recipe-list"), data=payload
        )
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertEqual(product_count, Product.objects.all().count())

    def test_update(self):
        recipe = RecipeFactory(owner=self.user)
        payload = {
            "ingredients": [
                {
                    "product": {"name": "Test product"},
                    "measure_type": MeasureType.G,
                    "amount": 200.5,
                }
            ]
        }
        response = self._patch(
            reverse("cooklist-api-v1-recipes:Recipe-detail", args=[recipe.id]),
            data=payload,
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(
            payload["ingredients"][0]["product"]["name"].lower(),
            response.json()["ingredients"][0]["product"]["name"],
        )

    def test_destroy(self):
        response = self._delete(
            reverse("cooklist-api-v1-recipes:Recipe-detail", args=[self.recipe.id]),
            user=self.user,
        )
        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)


class TestScheduledRecipeApi(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.recipe = RecipeFactory(owner=self.user)
        self.scheduled_recipe = ScheduledRecipeFactory(
            recipe=self.recipe, owner=self.user
        )

    def test_create(self):
        payload = {
            "owner": self.user.id,
            "recipe": self.recipe.id,
            "date": str(now()).split(" ")[0],
            "meal_type": MealType.BREAKFAST,
        }
        response = self._post(
            reverse("cooklist-api-v1-recipes:ScheduledRecipe-list"), data=payload
        )
        self.assertEqual(HTTP_201_CREATED, response.status_code)

    def test_delete(self):
        response = self._delete(
            reverse(
                "cooklist-api-v1-recipes:ScheduledRecipe-detail",
                args=[self.scheduled_recipe.id],
            ),
            user=self.user,
        )
        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)

    def test_list(self):
        response = self._get(
            reverse(
                "cooklist-api-v1-recipes:ScheduledRecipe-list",
            ),
            user=self.user,
        )
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.json()))
        data = response.json()[0]
        self.assertEqual(self.scheduled_recipe.meal_type, data["meal_type"])
        self.assertEqual(
            self.scheduled_recipe.recipe.owner.first_name,
            data["recipe"]["owner"]["first_name"],
        )
