from django import template

from recipes.models import Favorite, Purchase

register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.value in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.value)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.value)

    return new_request.urlencode()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    """ фильтр проверки находится ли рецепт в избранном """
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_purchase')
def is_purchase(recipe, user):
    """ фильтр проверки находится ли рецепт в списке покупок """
    return Purchase.objects.filter(user=user, recipe=recipe).exists()
