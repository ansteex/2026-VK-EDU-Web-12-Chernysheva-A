from django import forms
from django.utils.text import slugify

from .models import Answer, Question, Tag


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        label='Теги',
        help_text='Укажите не более трёх тегов через запятую.',
    )

    class Meta:
        model = Question
        fields = ('title', 'text')
        labels = {
            'title': 'Заголовок вопроса',
            'text': 'Текст вопроса',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_tags(self):
        tags = [tag.strip().lower() for tag in self.cleaned_data['tags'].split(',')]
        tags = [tag for tag in tags if tag]

        if not tags:
            raise forms.ValidationError('Укажите хотя бы один тег.')

        if len(tags) > 3:
            raise forms.ValidationError('Можно указать не более трёх тегов.')

        if any(len(tag) > 50 for tag in tags):
            raise forms.ValidationError('Название тега не должно быть длиннее 50 символов.')

        if any(not slugify(tag, allow_unicode=True) for tag in tags):
            raise forms.ValidationError('Введите корректные названия тегов.')

        return tags

    def save(self, author, commit=True):
        question = super().save(commit=False)
        question.author = author

        if commit:
            question.save()
            tags = []
            for name in self.cleaned_data['tags']:
                tag, _ = Tag.objects.get_or_create(
                    slug=slugify(name, allow_unicode=True),
                    defaults={'name': name},
                )
                tags.append(tag)
            question.tags.set(tags)

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        labels = {'text': 'Ваш ответ'}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
            }),
        }

    def save(self, author, question, commit=True):
        answer = super().save(commit=False)
        answer.author = author
        answer.question = question

        if commit:
            answer.save()

        return answer
