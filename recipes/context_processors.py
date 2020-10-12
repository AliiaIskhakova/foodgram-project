from .models import Purchase


def disable(request):
    """ для подсвечивания заголовка списка покупок,
    если список покупок пуст, заголовок раздела будет прозрачный """
    if request.user.is_authenticated:
        disable = Purchase.objects.filter(user=request.user).exists()
    else:
        disable = True
    return {'disable': disable}


def counter(request):
    """ счетчик для списка покупок в заголовке  """
    if request.user.is_authenticated:
        count = Purchase.objects.filter(user=request.user).count()
    else:
        count = []
    return {'count': count}
