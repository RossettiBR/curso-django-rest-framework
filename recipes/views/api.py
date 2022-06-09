
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializers = RecipeSerializer(instance=recipes, many=True)
    return Response(serializers.data)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serialized = RecipeSerializer(instance=recipe, many=False)
    return Response(serialized.data)
