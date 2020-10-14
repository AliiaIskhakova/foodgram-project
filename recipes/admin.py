from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, Purchase, Recipe,
                     RecipeIngredient, Tag)


class RecipeIngredient(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at',)
    inlines = (RecipeIngredient, )
    list_filter = ('title',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit',)
    list_filter = ('title',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Purchase, PurchaseAdmin)
