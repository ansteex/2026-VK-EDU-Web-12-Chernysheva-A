# Aski Haski

Учебный проект сервиса вопросов и ответов.

## Как запустить

1. Склонировать репозиторий.
2. Перейти в корень проекта.
3. Запустить локальный сервер (для Linux):

   ```bash
   python3 -m http.server 8000 --directory public
## Страницы

- `public/index.html` - список вопросов;
- `public/question.html` - страница вопроса и ответов;
- `public/ask.html` - создание вопроса;
- `public/login.html` - авторизация;
- `public/signup.html` - регистрация;
- `public/profile.html` - настройки профиля;
- `public/base.html` - пример общего макета страницы.
