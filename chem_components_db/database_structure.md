# Структура базы данных химических компонентов

## Описание каждой таблицы

### 1. Таблица Component (Компоненты)

**Назначение:** Основная таблица, хранит информацию о химических веществах.

| Поле | Тип БД | Тип Django | Обязательное | Описание |
|------|--------|-----------|------------|----------|
| id | INTEGER | AutoField | Да | Первичный ключ, автоматически увеличивается |
| name | VARCHAR(200) | CharField | Да | Название компонента (англ.), напр. "Water", "Ethanol" |
| formula | VARCHAR(100) | CharField | Да | Химическая формула, напр. "H2O", "C2H6O" |
| cas_number | VARCHAR(20) | CharField | Нет | CAS-номер (уникальный код вещества), напр. "7732-18-5" |
| molar_mass | FLOAT | FloatField | Да | Молярная масса в г/моль, напр. 18.015 |
| substance_class | VARCHAR(100) | CharField | Нет | Класс вещества: "спирт", "углеводород", "вода" и т.д. |
| normal_boiling_point | FLOAT | FloatField | Нет | Нормальная температура кипения в °C |
| critical_temperature | FLOAT | FloatField | Нет | Критическая температура в °C |
| critical_pressure | FLOAT | FloatField | Нет | Критическое давление в атм. |
| acentric_factor | FLOAT | FloatField | Нет | Ацентрический фактор Питцера (безразмерный) |

**Пример записи:**
```
Component(
    id=1,
    name="Water",
    formula="H2O",
    cas_number="7732-18-5",
    molar_mass=18.015,
    substance_class="Inorganic",
    normal_boiling_point=100.0,
    critical_temperature=374.0,
    critical_pressure=217.7,
    acentric_factor=0.344
)
```

---

### 2. Таблица DataSource (Источники данных)

**Назначение:** Справочник источников, из которых берутся свойства компонентов.

| Поле | Тип БД | Тип Django | Обязательное | Описание |
|------|--------|-----------|------------|----------|
| id | INTEGER | AutoField | Да | Первичный ключ |
| name | VARCHAR(200) | CharField | Да | Название источника, напр. "NIST", "Учебный датасет" |
| description | TEXT | TextField | Нет | Расширенное описание источника |
| url | VARCHAR(200) | URLField | Нет | Ссылка на источник (веб-адрес) |

**Пример записей:**
```
DataSource(id=1, name="NIST", url="https://www.nist.gov")
DataSource(id=2, name="Perry's Chemical Handbook", description="Справочник перити...")
DataSource(id=3, name="Manual entry", description="Ручной ввод данных")
```

---

### 3. Таблица ComponentAlias (Синонимы компонентов)

**Назначение:** Хранит альтернативные названия компонентов (русские, английские, из Aspen Plus, из HYSYS).

**Отношение:** Many-to-One к Component (FK component_id)

| Поле | Тип БД | Тип Django | Обязательное | Описание |
|------|--------|-----------|------------|----------|
| id | INTEGER | AutoField | Да | Первичный ключ |
| component_id | INTEGER (FK) | ForeignKey | Да | Ссылка на Component (удаление = CASCADE) |
| alias_name | VARCHAR(200) | CharField | Да | Альтернативное название вещества |
| alias_type | VARCHAR(10) | CharField | Да | Тип названия: 'ru', 'en', 'aspen', 'hysys' |

**Пример для Water (component_id=1):**
```
ComponentAlias(id=1, component_id=1, alias_name="Вода", alias_type="ru")
ComponentAlias(id=2, component_id=1, alias_name="Aqua", alias_type="en")
ComponentAlias(id=3, component_id=1, alias_name="WATER", alias_type="aspen")
ComponentAlias(id=4, component_id=1, alias_name="WATER", alias_type="hysys")
```

**Использование:** Когда вторая команда (Aspen/HYSYS) ищет компонент по названию "WATER", находит alias_type="aspen", получает component_id=1 и данные Water из Component.

---

### 4. Таблица Property (Свойства компонентов)

**Назначение:** Хранит дополнительные физико-химические свойства компонентов.

**Отношение:** Many-to-One к Component (FK component_id), Many-to-One к DataSource (FK source_id, optional)

| Поле | Тип БД | Тип Django | Обязательное | Описание |
|------|--------|-----------|------------|----------|
| id | INTEGER | AutoField | Да | Первичный ключ |
| component_id | INTEGER (FK) | ForeignKey | Да | Ссылка на Component (CASCADE) |
| property_name | VARCHAR(200) | CharField | Да | Название свойства: "плотность", "вязкость", "теплоёмкость" |
| value | FLOAT | FloatField | Да | Численное значение свойства |
| unit | VARCHAR(50) | CharField | Да | Единица измерения: "г/см³", "cP", "J/mol·K" |
| conditions | VARCHAR(200) | CharField | Нет | Условия измерения: "20°C, 1 атм" |
| source_id | INTEGER (FK) | ForeignKey | Нет | Ссылка на DataSource (SET_NULL if deleted) |

**Пример для Water:**
```
Property(
    id=1, component_id=1, property_name="Density",
    value=1.0, unit="g/cm³", conditions="20°C, 1 atm", source_id=1
)
Property(
    id=2, component_id=1, property_name="Viscosity",
    value=1.002, unit="cP", conditions="20°C", source_id=1
)
```

---

### 5. Таблица ImportLog (Журнал импорта)

**Назначение:** Записывает результаты загрузки данных из CSV/Excel файлов (используется Участником 3).

**Отношение:** Независимая таблица (не связана FK с другими)

| Поле | Тип БД | Тип Django | Обязательное | Описание |
|------|--------|-----------|------------|----------|
| id | INTEGER | AutoField | Да | Первичный ключ |
| imported_at | TIMESTAMP | DateTimeField | Да | Дата/время импорта (автоматически при создании) |
| file_name | VARCHAR(200) | CharField | Да | Имя загруженного файла: "components_v1.csv" |
| total_rows | INTEGER | IntegerField | Да | Всего строк в файле |
| success_count | INTEGER | IntegerField | Да | Успешно загружено строк |
| error_count | INTEGER | IntegerField | Да | Количество ошибок |
| errors | TEXT (JSON) | TextField | Нет | JSON со списком ошибок по строкам |

**Пример:**
```
ImportLog(
    id=1,
    imported_at="2026-07-12 15:30:00",
    file_name="components_demo.csv",
    total_rows=30,
    success_count=28,
    error_count=2,
    errors='[
        {"row": 5, "error": "Invalid molar_mass value"},
        {"row": 18, "error": "Duplicate cas_number"}
    ]'
)
```

---

## Логика связей (Constraints)

### CASCADE vs SET_NULL

- **Component → ComponentAlias (CASCADE):** Если удалить компонент, удалятся ВСЕ его синонимы автоматически (логично — синоним без компонента не имеет смысла)

- **Component → Property (CASCADE):** Если удалить компонент, удалятся все его свойства

- **DataSource → Property (SET_NULL):** Если удалить источник, свойства останутся, но поле source_id станет NULL (информация о свойстве сохранится, но источник забудется)

- **ImportLog:** Самостоятельная таблица, не связана с другими. Служит только журналом.

---

## Индексы и уникальность

- **Component.cas_number:** Рекомендуется уникален (один CAS-номер = одно вещество), но может быть пусто (для веществ без номера)

- **Component.name + formula:** Уникальная комбинация (одна пара название-формула = один компонент)

- **ComponentAlias:** Может быть несколько одинаковых имён, если они разных типов (напр., "WATER" может быть и в Aspen, и в HYSYS)

---

## Ограничения данных

1. **Обязательные поля** (NOT NULL в SQL):
   - Component: name, formula, molar_mass
   - ComponentAlias: component_id, alias_name, alias_type
   - Property: component_id, property_name, value, unit
   - DataSource: name
   - ImportLog: imported_at, file_name, total_rows, success_count, error_count

2. **Опциональные поля** (NULL допускается):
   - Component: cas_number, substance_class, boiling_point, critical_temp/pressure, acentric_factor
   - DataSource: description, url
   - Property: conditions, source_id
   - ImportLog: errors

3. **Типы данных и диапазоны:**
   - FloatField: положительные вещественные числа (молярная масса, температура)
   - CharField(max_length=N): текст, не более N символов
   - TextField: большие текстовые блоки (JSON-ошибки в ImportLog)

---

## Использование в системе

### Для веб-интерфейса (Участник 2)
- Показывает список Component
- При клике открывает detail: полные данные Component + все Property + все ComponentAlias

### Для импорта (Участник 3)
- Парсит CSV → создаёт/обновляет Component, Property
- Записывает результат в ImportLog

### Для API (Участник 4)
- /api/components/search/?name=WATER → ищет в ComponentAlias и Component → возвращает JSON Component

### Для Aspen/HYSYS команды (вторая команда)
- Обращается к API
- Получает Component данные
- Сравнивает с данными из расчётной схемы
