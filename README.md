# Сервис Foodgram

Foodgram — база рецептов. Здесь можно создавать свои рецепты, подписываться на других авторов. Есть страничка для избранного, а так же можно составлять список продуктов на основе выбранных рецептов с последующей выгрузкой. Реализована фильтрация рецептов по тегам. Проект можно развернуть в трех Docker-контейнерах с помощью docker-compose.

### Стэк используемых технологий



### Как развернуть проект с помощью docker-compose

1. Склонируйте репозиторий.
2. Перейдите в директорию проекта

```
cd foodgram-project
```

3. Соберите контейнеры и запустите их в фоновом режиме

```
docker-compose build
```
```
docker-compose up -d
```

4. Создайте и примените миграции в контейнере проекта 

```
docker-compose exec web python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```

5. Соберите статику

```
docker-compose exec web python manage.py collectstatic
```

6. Создайте суперпользователя

```
docker-compose exec web python manage.py createsuperuser
```
