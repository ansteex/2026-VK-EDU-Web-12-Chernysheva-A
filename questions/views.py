from django.shortcuts import get_object_or_404, render

from .models import Question, Tag
from .utils import paginate


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
    page = paginate(question.answers.with_details().order_by('-rating'), request)
    return render(request, 'questions/question.html', {
        'question': question, 'answers': page.object_list, 'page_obj': page,
    })


def ask(request):
    return render(request, 'questions/ask.html')
