from django.urls import include, path
from recipes import views
from rest_framework.routers import SimpleRouter

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.RecipeAPIv2ViewSet,
    basename='recipe-api'
)

print(recipe_api_v2_router.urls)
urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name="search"
    ),
    path(
        'recipes/tags/<slug:slug>/',
        views.RecipeListViewTag.as_view(),
        name="tag"
    ),
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(), name="category"),
    path('recipe/<int:pk>/', views.RecipeDetail.as_view(), name="recipe"),
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name="recipe_api_v1"
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipe_api_v1_detail",
    ),
    path('recipes/theory/', views.theory, name="theory"),
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.tag_api_detail,
        name='recipe_api_v2_tag',
    ),
    path('', include(recipe_api_v2_router.urls))
]