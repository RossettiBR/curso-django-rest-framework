import os

from django.db.models import Q
from django.http import JsonResponse
from django.http import Http404
from utils.pagination import make_pagination
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from tag.models import Tag
from django.forms.models import model_to_dict
from recipes.models import Recipe


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def theory(request, *args, **kwargs):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes
    }
    return render(
        request,
        'recipes/pages/theory.html',
        context=context
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )
        context.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_dict = recipes.object_list.values()

        return JsonResponse(
            list(recipes_dict),
            safe=False,
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': f'{context.get("recipes")[0].category.name} - Category | '
        })
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category_id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404
        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name: str = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        context.update({
            'page_title': f'Search for "{search_term}" ',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })
        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)

        if not qs:
            raise Http404

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'is_detail_page': True,
        })
        return context


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['update_at'] = str(recipe.update_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                 recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_step_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False
        )


class RecipeListViewTag(RecipeListViewBase):
    template_name: str = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            tags__slug=self.kwargs.get('slug', '')
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag '

        context.update({
            'page_title': f'"{page_title}" ',
        })
        return context
