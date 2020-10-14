"""foodgram URL Configuration"""

from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

urlpatterns = [

    path('admin/', admin.site.urls),  # админка

    path('auth/', include("users.urls")),  # регистрация и авторизация

    # если нужного шаблона для /auth не нашлось в файле users.urls —
    # ищем совпадения в файле django.contrib.auth.urls
    path('auth/', include("django.contrib.auth.urls")),

    # обработчик для главной ищем в приложении recipes
    path('', include("recipes.urls")),

]

urlpatterns += [
    # flatpages
    path(
        'about-author/',
        views.flatpage, {'url': '/about-author/'},
        name='about-author'
        ),

    path(
        'about-spec/',
        views.flatpage, {'url': '/about-spec/'},
        name='about-spec'
        ),

]

handler404 = "recipes.views.page_not_found"
handler500 = "recipes.views.server_error"
