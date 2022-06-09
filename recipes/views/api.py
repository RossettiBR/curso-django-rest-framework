
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from tag.models import Tag
from ..serializers import TagSerializer


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializers = RecipeSerializer(
        instance=recipes,
        many=True,
        context={'request': request},
    )
    return Response(serializers.data)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serialized = RecipeSerializer(
        instance=recipe,
        many=False,
        context={'request': request},
    )
    return Response(serialized.data)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
