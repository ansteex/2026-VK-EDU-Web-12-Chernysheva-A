from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField('название', max_length=50, unique=True)
    slug = models.SlugField('адрес', max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def with_details(self):
        return (
            self.get_queryset()
            .select_related('author', 'author__profile')
            .prefetch_related('tags')
            .annotate(answers_count=Count('answers', distinct=True))
        )

    def new(self):
        return self.with_details().order_by('-created_at')

    def best(self):
        return self.with_details().order_by('-rating', '-created_at')

    def by_tag(self, tag):
        return self.with_details().filter(tags=tag).order_by('-created_at')


class Question(models.Model):
    title = models.CharField('заголовок', max_length=150)
    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='автор',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='questions',
        verbose_name='теги',
    )
    rating = models.IntegerField('рейтинг', default=0)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)

    objects = QuestionManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questions:question', kwargs={'question_id': self.pk})


class AnswerManager(models.Manager):
    def with_details(self):
        return self.get_queryset().select_related('author', 'author__profile')


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='вопрос',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='автор',
    )
    text = models.TextField('текст')
    rating = models.IntegerField('рейтинг', default=0)
    is_correct = models.BooleanField('правильный ответ', default=False)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)

    objects = AnswerManager()

    class Meta:
        ordering = ['created_at']
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return f'Ответ на вопрос «{self.question.title}»'


class QuestionLike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUES = ((LIKE, 'Нравится'), (DISLIKE, 'Не нравится'))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_likes',
        verbose_name='пользователь',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='вопрос',
    )
    value = models.SmallIntegerField('оценка', choices=VALUES, default=LIKE)

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = 'оценка вопроса'
        verbose_name_plural = 'оценки вопросов'

    def __str__(self):
        return f'{self.user}: {self.question} ({self.value})'


class AnswerLike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUES = ((LIKE, 'Нравится'), (DISLIKE, 'Не нравится'))

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answer_likes',
        verbose_name='пользователь',
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='ответ',
    )
    value = models.SmallIntegerField('оценка', choices=VALUES, default=LIKE)

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = 'оценка ответа'
        verbose_name_plural = 'оценки ответов'

    def __str__(self):
        return f'{self.user}: ответ {self.answer_id} ({self.value})'
