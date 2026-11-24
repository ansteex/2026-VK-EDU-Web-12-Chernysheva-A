from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnswerForm, QuestionForm
from .models import Question, Tag
from .utils import paginate


ANSWERS_PER_PAGE = 10


def index(request):
    page = paginate(Question.objects.new(), request)
    return render(request, 'questions/index.html', {
        'questions': page.object_list, 'page_obj': page,
    })


def hot(request):
    page = paginate(Question.objects.best(), request)
    return render(request, 'questions/hot.html', {
        'questions': page.object_list, 'page_obj': page,
    })


def tag_questions(request, tag):
    tag_obj = get_object_or_404(Tag, slug=tag)
    page = paginate(Question.objects.by_tag(tag_obj), request)
    return render(request, 'questions/tag.html', {
        'questions': page.object_list, 'page_obj': page, 'tag': tag_obj,
    })


def question_detail(request, question_id):
    question = get_object_or_404(Question.objects.with_details(), pk=question_id)

    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    form = AnswerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        answer = form.save(request.user, question)
        answers_count = question.answers.count()
        page_number = (answers_count - 1) // ANSWERS_PER_PAGE + 1
        return redirect(
            f'{question.get_absolute_url()}?page={page_number}#answer-{answer.pk}'
        )

    answers = question.answers.with_details().order_by('created_at', 'id')
    page = paginate(answers, request, per_page=ANSWERS_PER_PAGE)
    return render(request, 'questions/question.html', {
        'question': question,
        'answers': page.object_list,
        'page_obj': page,
        'form': form,
    })


@login_required
def ask(request):
    form = QuestionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        question = form.save(request.user)
        return redirect(question)

    return render(request, 'questions/ask.html', {'form': form})
