from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название ингридиента')
    unit = models.CharField(
        max_length=20, default='', verbose_name='Eдиница измерения')


class Tag(models.Model):
    value = models.CharField('Значение на английском', max_length=50)
    # orange, green, purple
    style = models.CharField('Цвет в шаблоне', max_length=50, null=True)
    # Завтрак, Обед, Ужин
    name = models.CharField('Имя в шаблоне', max_length=50, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='static/upload_images/', verbose_name='Выбрать файл')
    description = models.TextField(verbose_name='Рецепт')
    ingredients = models.ManyToManyField(
        Ingredient, through='Recipeingredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингридиент')
    tag = models.ManyToManyField(Tag, related_name='tag')
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at', ]


class Recipeingredient(models.Model):
    """ связывающая таблица """
    amount = models.PositiveIntegerField(default=0)  # количество ингредиента
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient.unit


class Favorite(models.Model):
    # кто добавляет в избранное
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_by', default='')
    # рецепт, который добавляют в избранное
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite', default='')


class Follow(models.Model):
    #  пользователь, который подписывается
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")
    #  пользователь, на которого подписываются
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        ordering = ['-id', ]


class Purchase(models.Model):
    # чей список покупок
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner')
    # рецепт, ингридиенты которого добавлены в список покупок
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
