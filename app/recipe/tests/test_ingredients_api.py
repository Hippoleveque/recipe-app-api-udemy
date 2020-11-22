from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """Test the public API for ingredients"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_ingredients_unauthorized(self):
        "Test that authentication is required for ingredients"

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private API for ingredients"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_success(self):
        """Test retrieving ingredients"""
        Ingredient.objects.create(name="Salt", user=self.user)
        Ingredient.objects.create(name="Pepper", user=self.user)

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that retrieved ingredients are limited to current user"""
        other_user = get_user_model().objects.create_user(
            "test2@test.com",
            "test123",
        )

        Ingredient.objects.create(name="Salt", user=other_user)
        ingredient = Ingredient.objects.create(name="Pepper", user=self.user)

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.data[0]["name"], ingredient.name)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient successfully"""
        payload = {"name": "Salt"}

        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating a new ingredient with invalid payload"""
        payload = {"name": ""}

        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
