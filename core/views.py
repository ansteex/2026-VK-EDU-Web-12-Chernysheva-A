from django.http import HttpResponse


def login_view(request):
    return HttpResponse('Страница входа')


def signup(request):
    return HttpResponse('Страница регистрации')


def profile(request):
    return HttpResponse('Настройки профиля')
