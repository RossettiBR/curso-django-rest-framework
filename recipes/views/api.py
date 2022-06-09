
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe


@api_view()
def recipe_api_list(request):
    return Response({
        "name": 'blablalba'
    })
