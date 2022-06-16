from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def teste_recipe_api_list_returns_status_code_200(self):
        api_url = reverse('recipes:recipe-api-list')
        response = self.client.get(api_url)
        self.assertEqual(
            response.status_code,
            200
        )
