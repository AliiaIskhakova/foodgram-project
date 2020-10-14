from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


def generate_shop_list(request):
    """ генерирует список покупок для выгрузки """

    # для кого формируется список покупок
    user = get_object_or_404(User, username=request.user.username)
    # рецепты, ингридиенты которого составят список покупок
    shop_list = user.purchases.all()
    ingredients = {}  # словарь для списка покупок

    for item in shop_list:
        for elem in item.recipe.recipeingredient_set.all():

            name = f'{elem.ingredient.title} ({elem.ingredient.unit})'
            units = elem.amount

            # суммирование кол-ва продуктов, если они дублируются
            ingredients[name] = ingredients.get(name, 0) + units

    # формирование из словаря удобоваримого списка на выгрузку
    ingredients_download = []

    for key, units in ingredients.items():
        ingredients_download.append(f'{key} - {units}, ')

    return ingredients_download


def get_ingredients(request):
    """ генерирует список ингредиентов при создании/редактировании рецепта,
    достает из POST запроса"""

    ingredients = {}  # словарь для списка ингредиентов

    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]  # получаем количество
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
                ]

    return ingredients
