
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializers = RecipeSerializer(instance=recipes, many=True)
    return Response(serializers.data)


@api_view()
def recipe_api_detail(request, pk):
    recipes = Recipe.objects.filter(pk=pk)
    serialized = RecipeSerializer(instance=recipes, many=False)
    return Response(serialized.data)
