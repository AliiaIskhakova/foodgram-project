import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import RecipeForm
from .models import (Favorite, Follow, Ingredient, Purchase, Recipe,
                     RecipeIngredient, Tag)
from .utils import generate_shop_list, get_ingredients

User = get_user_model()


def index(request):
    """ главная страница """
    all_tags = Tag.objects.all()
    active_index = True  # для подсвечивания активного раздела

    tag_value = request.GET.getlist('filters')
    if tag_value:
        recipes = Recipe.objects.filter(
            tag__value__in=tag_value).distinct()
    else:
        recipes = Recipe.objects.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page': page, 'paginator': paginator, 'all_tags': all_tags,
        'active_index': active_index})


def recipe_single(request, recipe_id, username):
    """страница просмотра рецепта"""
    # рецепт, который нужно отобразить
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, username=username)  # автор рецепта

    # проверяем, подписан ли текущий юзер на автора
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author).exists()

    return render(request, 'single_page.html', {
        'recipe': recipe, 'following': following})


def profile(request, username):
    """ страница автора рецептов """
    author = get_object_or_404(User, username=username)  # автор, чья страница
    all_tags = Tag.objects.all()

    tag_value = request.GET.getlist('filters')
    if tag_value:
        recipes = Recipe.objects.filter(
            tag__value__in=tag_value, author=author).distinct()
    else:
        recipes = Recipe.objects.filter(author=author)

    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=author).exists()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'author_profile.html', {
        'page': page, 'paginator': paginator, 'following': following,
        'all_tags': all_tags, 'author': author})


@login_required
def follow_index(request, username):
    """страница Мои подписки"""
    follow = get_object_or_404(User, username=username)  # кто подписывается
    # авторы, на которых подписан
    authors = Follow.objects.filter(user=follow)
    active_follow = True  # для подсвечивания активного раздела

    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'my_follow.html', {
        'page': page, 'paginator': paginator, 'follow': follow,
        'active_follow': active_follow, 'authors': authors})


@login_required
def favorites_index(request, username):
    """страница просмотра избранного"""
    all_tags = Tag.objects.all()
    active_favorites = True  # для подсвечивания активного раздела

    tag_value = request.GET.getlist('filters')
    if tag_value:
        favorites = Recipe.objects.filter(
            tag__value__in=tag_value, favorite__user__id=request.user.id
            ).distinct()
    else:
        favorites = Recipe.objects.filter(favorite__user__id=request.user.id)

    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'favorite.html', {
        'page': page, 'paginator': paginator, 'all_tags': all_tags,
        'active_favorites': active_favorites})


@login_required
def purchases_index(request):
    """страница списка покупок"""
    purchases = Purchase.objects.filter(user=request.user)

    return render(request, 'shop_list.html', {
        'purchases': purchases})


@login_required
def new_recipe(request):
    """ создание нового рецепта """
    active_new_recipe = True  # для подсвечивания активного раздела

    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        # функция, передающая список ингредиентов
        ingredients = get_ingredients(request)

        if not ingredients: 
            form.add_error(None, 'Добавьте хотя бы один ингредиент')
        elif form.is_valid():
            # сохраняем форму, но не отправляем в БД
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user  # получаем автора нового рецепта
            new_recipe.save()  # сохраняем новый рецепт

            # заполнение связной таблицы в БД
            for item in ingredients:
                RecipeIngredient.objects.create(
                    amount=ingredients[item],
                    recipe=new_recipe,
                    ingredient=get_object_or_404(Ingredient, title=f'{item}'))

            # сохраняем данные для полей м2м (тэги и ингредиенты)
            form.save_m2m()
            return redirect('recipes:index')
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None)

    return render(request, 'new_recipe.html', {
        'form': form, 'active_new_recipe': active_new_recipe})


class Ingredients(View):
    """ нужен для автозаполнения поля ингредиентов
    в форме создания/редактирования рецепта """

    def get(self, request):
        text = request.GET['query']

        ingredients = list(Ingredient.objects.filter(
            title__icontains=text).values('title', 'unit'))

        return JsonResponse(ingredients, safe=False)


def recipe_edit(request, recipe_id):
    """страница редактирования рецепта"""
    # получаем рецепт, который редактируем
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        form = RecipeForm(request.POST or None, files=request.FILES or None,
                        instance=recipe)
        # функция, передающая список ингредиентов
        ingredients = get_ingredients(request)

        if not ingredients: 
            form.add_error(None, 'Добавьте хотя бы один ингредиент')
        elif form.is_valid():
            # удаляем ингредиенты, связанные с рецептом
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            # сохраняем форму, но не отправляем в БД
            recipe = form.save(commit=False)
            recipe.author = request.user  # получаем автора рецепта
            recipe.save()  # сохраняем изменения

            # заполнение связной таблицы обновленным списком ингредиентов
            for item in ingredients:
                RecipeIngredient.objects.create(
                    amount=ingredients[item],
                    recipe=recipe,
                    ingredient=get_object_or_404(Ingredient, title=f'{item}'))

            # сохраняем данные для полей м2м (тэги и ингредиенты)
            form.save_m2m()
            return redirect('recipes:index')
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None,
                          instance=recipe)

    return render(request, 'change_recipe.html', {
        'form': form, 'recipe': recipe})


def recipe_delete(request, recipe_id):
    """удаление рецепта"""
    # получаем рецепт, который хотим удалить
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # если текущий юзер является автором рецепта, то удаляем рецепт
    if request.user == recipe.author:
        recipe.delete()

    return redirect('recipes:index')

def purchases_delete(request, recipe_id):
    """ удаление рецепта из списка покупок """
    # получаем рецепт, который хотим удалить
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # удаляем рецепт из списка
    Purchase.objects.filter(user=request.user, recipe=recipe
                                ).delete()

    return redirect('recipes:purchases_index')


class Subscribe(View):
    """ Подписки добавить/удалить """

    def post(self, request):
        """ подписка на пользователя """
        # получаем id пользователя, на которого хотим подписаться
        author_id = json.loads(request.body)['id']
        # получаем пользователя, на которого хотим подписаться
        author = get_object_or_404(User, id=author_id)

        Follow.objects.get_or_create(user=request.user, author=author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        """ отписка от пользователя """
        # находим пользователя, от которого хотим отписаться
        author = get_object_or_404(User, id=author_id)
        # удаляем из подписок фолловера пользователя,
        # от которого хотим отписаться
        Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({'success': True})


class Favorites(View):
    """ Избранное добавить/удалить """

    def post(self, request):
        """ добавление в избранное """
        # получаем id рецепта, которого хотим добавить в избранное
        recipe_id = json.loads(request.body)['id']
        # получаем рецепт, который хотим добавить в избранное
        recipe = get_object_or_404(Recipe, id=recipe_id)

        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        """ удаление из избранного """
        # находим рецепт, который хотим удалить
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # удаляем рецепт из избранного текущего пользователя
        Favorite.objects.filter(user=request.user, recipe=recipe
                                ).delete()
        return JsonResponse({'success': True})


class Purchases(View):
    """ Список покупок добавить/удалить """

    def post(self, request):
        """ добавление в список покупок """
        # получаем id рецепта,
        # ингредиенты которого хотим добавить в список покупок
        recipe_id = json.loads(request.body)['id']
        # получаем рецепт, ингредиенты которого хотим добавить в список покупок
        recipe = get_object_or_404(Recipe, id=recipe_id)

        Purchase.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        """ удаление из списка покупок """
        # находим рецепт, который хотим удалить из списка покупок
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # удаляем искомый рецепт из списка текущего юзера
        Purchase.objects.filter(user=request.user, recipe=recipe
                                ).delete()

        return JsonResponse({'success': True})


@login_required
def download(request):
    """скачивание списка покупок"""
    # функция, формирующая список покупок
    result = generate_shop_list(request)
    filename = 'shop_list.txt'
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
                                                                    filename)
    return response


def page_not_found(request, exception):
    #  переменная exception содержит отладочную информацию,
    #  выводить её в шаблон пользовательской страницы 404 не нужно
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
