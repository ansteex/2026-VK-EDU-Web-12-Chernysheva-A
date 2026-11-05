from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render


AVATARS = (
    'img/avatar.png',
    'img/avatar1.png',
    'img/avatar2.png',
)

VOTE_STATES = ('liked', 'disliked', None)

TAG_SETS = (
    (
        {'name': 'Python', 'slug': 'python'},
        {'name': 'Django', 'slug': 'django'},
    ),
    (
        {'name': 'HTML', 'slug': 'html'},
        {'name': 'CSS', 'slug': 'css'},
    ),
    (
        {'name': 'C++', 'slug': 'cpp'},
        {'name': 'Операционная система', 'slug': 'os'},
    ),
)

QUESTION_LIST = [
    {
        'id': number,
        'title': f'Вопрос №{number}: как устроен процесс в операционной системе?',
        'text': (
            'Помогите разобраться с процессами, памятью и режимами '
            'выполнения в операционной системе.'
        ),
        'avatar': AVATARS[(number - 1) % len(AVATARS)],
        'rating': number % 11,
        'answers_count': number % 5,
        'created_at': '4 ноября 2026, 12:30',
        'vote_state': VOTE_STATES[(number - 1) % len(VOTE_STATES)],
        'tags': TAG_SETS[(number - 1) % len(TAG_SETS)],
    }
    for number in range(1, 31)
]

ANSWER_LIST = [
    {
        'id': number,
        'author': f'Пользователь {number}',
        'text': (
            f'Ответ №{number}. Процесс может выполняться в пользовательском '
            'режиме или в режиме ядра операционной системы.'
        ),
        'avatar': AVATARS[number % len(AVATARS)],
        'rating': (65 - number) % 17,
        'created_at': '4 ноября 2026, 13:00',
        'vote_state': VOTE_STATES[number % len(VOTE_STATES)],
        'is_correct': number == 1,
    }
    for number in range(1, 66)
]


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def index(request):
    page = paginate(QUESTION_LIST, request, per_page=5)
    context = {
        'questions': page.object_list,
        'page_obj': page,
    }
    return render(request, 'questions/index.html', context)


def hot(request):
    questions = sorted(
        QUESTION_LIST,
        key=lambda question: question['rating'],
        reverse=True,
    )
    page = paginate(questions, request, per_page=5)
    context = {
        'questions': page.object_list,
        'page_obj': page,
    }
    return render(request, 'questions/hot.html', context)


def tag_questions(request, tag):
    questions = [
        question
        for question in QUESTION_LIST
        if any(question_tag['slug'] == tag for question_tag in question['tags'])
    ]
    page = paginate(questions, request, per_page=5)
    context = {
        'questions': page.object_list,
        'page_obj': page,
        'tag': tag,
    }
    return render(request, 'questions/tag.html', context)


def question_detail(request, question_id):
    question = next(
        (
            question
            for question in QUESTION_LIST
            if question['id'] == question_id
        ),
        None,
    )
    if question is None:
        raise Http404('Вопрос не найден')

    answers = sorted(
        ANSWER_LIST,
        key=lambda answer: answer['rating'],
        reverse=True,
    )
    page = paginate(answers, request, per_page=30)
    context = {
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
    }
    return render(request, 'questions/question.html', context)


def ask(request):
    return render(request, 'questions/ask.html')
