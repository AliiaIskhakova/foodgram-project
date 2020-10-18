# Сервис Foodgram

Foodgram — база рецептов. Здесь можно создавать свои рецепты, подписываться на других авторов. Есть страничка для избранного, а так же можно составлять список продуктов на основе выбранных рецептов с последующей выгрузкой. Реализована фильтрация рецептов по тегам. Проект можно развернуть в трех Docker-контейнерах с помощью docker-compose.

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

4. В новом терминале зайдите в контейнер и создайте суперпользователя 

```
docker exec -it <CONTAINER ID> bash
```
```
python manage.py createsuperuser
```

5. Загрузите в базу тестовые данные

```
python manage.py loaddata fixtures.json
```
