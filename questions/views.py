from django.http import HttpResponse


def index(request):
    return HttpResponse('Новые вопросы')


def hot(request):
    return HttpResponse('Лучшие вопросы')


def tag_questions(request, tag):
    return HttpResponse(f'Вопросы по тегу: {tag}')


def question_detail(request, question_id):
    return HttpResponse(f'Вопрос №{question_id}')


def ask(request):
    return HttpResponse('Новый вопрос')
