# Инструкция для команды

## Приложение уже работает!

Веб-приложение развёрнуто на облаке:https://alisaboyarkina20.pythonanywhere.com/admin/
Логин: `admin`
Пароль: `admin123`

## Как работать локально

### 1. Клонируй проект

```bash
git clone https://github.com/AlisaBoyarkina/chem_components_db.git
cd chem_components_db
```

### 2. Создай окружение

```bash
python3 -m venv venv
source venv/bin/activate  # на Mac/Linux
# или venv\Scripts\activate на Windows
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

### 4. Создай локальную БД

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

### 5. Запусти сервер

```bash
python3 manage.py runserver
```

Откроется: http://127.0.0.1:8000/admin/

## Твоя роль в проекте

- **Участник 2** (Веб-интерфейс): работай в ветке `feature/web-interface`
- **Участник 3** (Импорт CSV): работай в ветке `feature/import-csv`
- **Участник 4** (REST API): работай в ветке `feature/rest-api`
- **Участник 5** (Тесты): работай в ветке `feature/tests-docs`

## Рабочий процесс

1. Переключись на свою ветку:
```bash
git checkout feature/твоя-ветка
```

2. Делай изменения в коде

3. Коммитишь:
```bash
git add .
git commit -m "Описание что сделал"
git push origin feature/твоя-ветка
```

4. Когда закончишь, сделай Pull Request на GitHub

## База данных

Все модели уже готовы (Участник 1 сделал):
- Component
- ComponentAlias
- Property
- DataSource
- ImportLog

Просто используй их в своем коде!

## Вопросы?

Смотри документацию:
- `README.md` — общее описание
- `ER_diagram.md` — схема БД
- `database_structure.md` — подробное описание таблиц
- `Next_Steps_for_Team.md` — план для каждого участника
