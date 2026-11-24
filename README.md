# Aski Haski

Учебный сервис вопросов и ответов на Django.

## Локальный запуск

Для локального запуска нужен установленный PostgreSQL.

1. Создать файл настроек:

   ```bash
   cp .env.example .env.local
   ```

2. Создать виртуальное окружение и установить зависимости:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Применить миграции и запустить сервер:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Запуск через Docker

1. Создать файл настроек Docker:

   ```bash
   cp .env.example .env.docker
   ```

2. В `.env.docker` заменить адрес базы:

   ```text
   POSTGRES_HOST=db
   ```

3. Собрать и запустить проект:

   ```bash
   docker compose up --build
   ```

4. Открыть сайт:

   ```text
   http://localhost:8000
   ```

Миграции применяются автоматически при запуске контейнера.

## Тестовые данные

Команда принимает коэффициент заполнения `ratio`:

```bash
docker compose exec web python manage.py fill_db 10
```

При `ratio=10` будут созданы:

- 10 пользователей и профилей;
- 100 вопросов;
- 1000 ответов;
- 10 тегов;
- 2000 оценок.

Для полного объёма из задания используется:

```bash
docker compose exec web python manage.py fill_db 10000
```

## Административная панель

Создать администратора:

```bash
docker compose exec web python manage.py createsuperuser
```

Админка доступна по адресу:

```text
http://localhost:8000/admin/
```

## Основные страницы

- `/` — новые вопросы;
- `/hot/` — лучшие вопросы;
- `/tag/python/` — вопросы по тегу;
- `/question/1/` — вопрос и ответы;
- `/admin/` — административная панель.

## Остановка проекта

```bash
docker compose down
```

Чтобы также удалить данные PostgreSQL:

```bash
docker compose down -v
```
