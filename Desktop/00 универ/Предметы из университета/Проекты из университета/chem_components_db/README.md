# Django Chemical Components Database

Веб-сервис для управления справочником химических компонентов. Часть учебного проекта по интеграции с Aspen Plus / HYSYS.

## Возможности

- ✅ Хранение информации о химических веществах (название, формула, молярная масса, критические параметры)
- ✅ Синонимы компонентов (русские, английские, Aspen Plus, HYSYS)
- ✅ Физико-химические свойства компонентов
- ✅ Django Admin для управления данными
- ✅ Источники данных (NIST, справочники, ручной ввод)
- ✅ Логирование импорта данных из CSV/Excel

## Быстрый старт

### 1. Клонировать проект

```bash
git clone https://github.com/AlisaBoyarkina/chem_components_db.git
cd chem_components_db
```

### 2. Создать виртуальное окружение

**На macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**На Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Применить миграции (создать БД)

```bash
python3 manage.py migrate
```

### 5. Создать суперпользователя (администратор)

```bash
python3 manage.py createsuperuser
```

Введи:
- Username: `admin`
- Email: `test@test.com`
- Password: любой пароль

### 6. Запустить сервер

```bash
python3 manage.py runserver
```

Сервер запустится на `http://127.0.0.1:8000/`

### 7. Зайти в админ-панель

Открой браузер: `http://127.0.0.1:8000/admin/`

Введи учётные данные суперпользователя.

## Структура проекта
chem_components_db/
├── config/              # Настройки Django
├── components/          # Приложение с моделями БД
│   ├── models.py       # Component, ComponentAlias, Property, DataSource, ImportLog
│   ├── admin.py        # Админ-панель
│   └── migrations/     # Миграции БД
├── manage.py           # Главный скрипт Django
├── db.sqlite3          # База данных (создаётся после migrate)
├── requirements.txt    # Зависимости Python
└── README.md          # Этот файл
## Модели БД

### Component
Основная таблица с информацией о химических веществах.

**Поля:** name, formula, cas_number, molar_mass, substance_class, normal_boiling_point, critical_temperature, critical_pressure, acentric_factor

### ComponentAlias
Синонимы компонентов (разные названия в разных системах).

**Типы:** ru (русское), en (английское), aspen (Aspen Plus), hysys (HYSYS)

### Property
Физико-химические свойства компонентов.

**Поля:** property_name, value, unit, conditions, source (DataSource)

### DataSource
Источники данных (NIST, справочники, ручной ввод).

### ImportLog
Журнал импорта данных из CSV/Excel.

## Документация

Подробное описание структуры БД: [database_structure.md](database_structure.md)

ER-диаграмма: [ER_diagram.md](ER_diagram.md)

План действий для остальной команды: [Next_Steps_for_Team.md](Next_Steps_for_Team.md)

## Технологии

- Python 3.12+
- Django 6.0.7
- SQLite
- Django Admin

## Участники проекта

- **Участник 1 (Алиса)** — Проектирование структуры БД, модели, миграции, админ-панель
- **Участник 2** — Web-интерфейс (список, карточка, поиск)
- **Участник 3** — Импорт данных из CSV/Excel
- **Участник 4** — REST API
- **Участник 5** — Тестирование и документация

## Решение проблем

### Ошибка "no such table"
БД не создана. Запусти:
```bash
python3 manage.py migrate
```

### Забыл пароль суперпользователя
Создай нового:
```bash
python3 manage.py createsuperuser
```

### Хочу очистить БД и начать заново
```bash
rm db.sqlite3
python3 manage.py migrate
python3 manage.py createsuperuser
```

## Версия

v1.0 — 12 июля 2026

## Лицензия

MIT (для учебного проекта)
