from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    # РЕЦЕПТ
    # страница просмотра рецепта
    path(
        '<username>/<int:recipe_id>', views.recipe_single,
        name='recipe_single'),
    # создание нового рецепта
    path('new/', views.new_recipe, name='new_recipe'),
    # редактирование рецепта
    path('<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    # удаление рецепта
    path('<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),

    # API JS
    # добавление рецепта в избранное
    path('api/favorites', views.Favorites.as_view(), name='add_favorites'),
    # удаление рецепта из избранного
    path(
        'api/favorites/<int:recipe_id>', views.Favorites.as_view(),
        name='remove_favorites'),

    # СТРАНИЦЫ
    path('', views.index, name="index"),
    # страница автора рецептов
    path('<username>/', views.profile, name='profile'),
    # страница просмотра подписок
    path('<username>/follow', views.follow_index, name='follow_index'),
    # страница просмотра избранного
    path(
        '<username>/favorites', views.favorites_index, name='favorites_index'),
    # страница списка покупок
    path('purchases', views.purchases_index, name='purchases_index'),

    # скачивание списка покупок
    path('download', views.download, name='download'),

    # API JS
    # запрос на подписку
    path('api/subscriptions', views.Subscribe.as_view(), name='add_follow'),
    # запрос на отписку
    path(
        'api/subscriptions/<int:author_id>', views.Subscribe.as_view(),
        name='remove_follow'),

    # добавление в список покупок
    path('api/purchases', views.Purchases.as_view(), name='add_purchases'),
    # удаление из списка покупок
    path(
        'api/purchases/<int:recipe_id>', views.Purchases.as_view(),
        name='remove_purchases'),

    # автозаполнение поля Ингредиенты при создании нового рецепта
    path('api/ingredients', views.Ingredients.as_view(), name='ingredients'),
]
