
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializers = RecipeSerializer(instance=recipes)
    return Response(serializers.data)
