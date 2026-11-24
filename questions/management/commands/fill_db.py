from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from core.models import Profile
from questions.models import (
    Answer,
    AnswerLike,
    Question,
    QuestionLike,
    Tag,
)


BATCH_SIZE = 5000


def create_in_batches(model, objects):
    batch = []

    for obj in objects:
        batch.append(obj)
        if len(batch) == BATCH_SIZE:
            model.objects.bulk_create(batch, batch_size=BATCH_SIZE)
            batch = []

    if batch:
        model.objects.bulk_create(batch, batch_size=BATCH_SIZE)


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными: fill_db [ratio]'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        if ratio < 1:
            raise CommandError('ratio должен быть положительным числом')

        fake = Faker('ru_RU')
        fake.seed_instance(42)

        self.stdout.write('Удаляем старые тестовые данные...')
        Question.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        password = make_password('password')
        users = (
            User(
                username=f'user{number}',
                email=f'user{number}@example.com',
                password=password,
            )
            for number in range(1, ratio + 1)
        )
        create_in_batches(User, users)
        user_ids = list(
            User.objects.filter(is_superuser=False)
            .order_by('id')
            .values_list('id', flat=True)
        )

        profiles = (
            Profile(
                user_id=user_id,
                avatar=(
                    'img/avatar.png'
                    if index % 7 == 0
                    else f'img/avatar{index % 7}.png'
                ),
            )
            for index, user_id in enumerate(user_ids)
        )
        create_in_batches(Profile, profiles)
        self.stdout.write(f'Пользователи: {len(user_ids)}')

        main_tags = ['Python', 'HTML', 'CSS', 'C++', 'Django']
        tags = (
            Tag(
                name=(
                    main_tags[index]
                    if index < len(main_tags)
                    else f'{fake.word()}-{index + 1}'
                ),
                slug=(
                    ['python', 'html', 'css', 'cpp', 'django'][index]
                    if index < len(main_tags)
                    else f'tag-{index + 1}'
                ),
            )
            for index in range(ratio)
        )
        create_in_batches(Tag, tags)
        tag_ids = list(Tag.objects.order_by('id').values_list('id', flat=True))
        self.stdout.write(f'Теги: {len(tag_ids)}')

        question_count = ratio * 10
        question_titles = [fake.sentence(nb_words=8) for _ in range(200)]
        question_texts = [fake.paragraph(nb_sentences=4) for _ in range(200)]
        questions = (
            Question(
                title=question_titles[index % len(question_titles)][:150],
                text=question_texts[index % len(question_texts)],
                author_id=user_ids[index % len(user_ids)],
                rating=index % 21 - 5,
            )
            for index in range(question_count)
        )
        create_in_batches(Question, questions)
        question_ids = list(
            Question.objects.order_by('id').values_list('id', flat=True)
        )

        question_tags = (
            Question.tags.through(
                question_id=question_id,
                tag_id=tag_ids[(index + offset) % len(tag_ids)],
            )
            for index, question_id in enumerate(question_ids)
            for offset in range(min(2, len(tag_ids)))
        )
        create_in_batches(Question.tags.through, question_tags)
        self.stdout.write(f'Вопросы: {len(question_ids)}')

        answer_count = ratio * 100
        answer_texts = [fake.paragraph(nb_sentences=3) for _ in range(500)]
        answers = (
            Answer(
                question_id=question_ids[index % len(question_ids)],
                author_id=user_ids[(index + 1) % len(user_ids)],
                text=answer_texts[index % len(answer_texts)],
                rating=index % 16 - 3,
                is_correct=index < len(question_ids),
            )
            for index in range(answer_count)
        )
        create_in_batches(Answer, answers)
        answer_ids = list(Answer.objects.order_by('id').values_list('id', flat=True))
        self.stdout.write(f'Ответы: {len(answer_ids)}')

        question_likes_per_user = min(50, len(question_ids))
        answer_likes_per_user = min(
            200 - question_likes_per_user,
            len(answer_ids),
        )

        question_likes = (
            QuestionLike(
                user_id=user_id,
                question_id=question_ids[(user_index + offset) % len(question_ids)],
                value=-1 if offset % 5 == 0 else 1,
            )
            for user_index, user_id in enumerate(user_ids)
            for offset in range(question_likes_per_user)
        )
        create_in_batches(QuestionLike, question_likes)

        answer_likes = (
            AnswerLike(
                user_id=user_id,
                answer_id=answer_ids[(user_index + offset) % len(answer_ids)],
                value=-1 if offset % 5 == 0 else 1,
            )
            for user_index, user_id in enumerate(user_ids)
            for offset in range(answer_likes_per_user)
        )
        create_in_batches(AnswerLike, answer_likes)

        likes_count = ratio * (
            question_likes_per_user + answer_likes_per_user
        )
        self.stdout.write(f'Оценки: {likes_count}')
        self.stdout.write(self.style.SUCCESS('База данных заполнена.'))
