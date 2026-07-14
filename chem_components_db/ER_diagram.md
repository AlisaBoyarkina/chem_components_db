# ER-диаграмма: База данных химических компонентов

## Визуальная схема связей

```
┌─────────────────────────┐
│      Component          │
├─────────────────────────┤
│ id (PK)                 │
│ name                    │
│ formula                 │
│ cas_number              │
│ molar_mass              │
│ substance_class         │
│ normal_boiling_point    │
│ critical_temperature    │
│ critical_pressure       │
│ acentric_factor         │
└─────────────────────────┘
          │
          │ 1:M
          ├─────────────────────────────────┐
          │                                 │
          ▼                                 ▼
┌──────────────────────────┐    ┌────────────────────────┐
│   ComponentAlias         │    │      Property          │
├──────────────────────────┤    ├────────────────────────┤
│ id (PK)                  │    │ id (PK)                │
│ component_id (FK)        │    │ component_id (FK)      │
│ alias_name               │    │ property_name          │
│ alias_type (choices)     │    │ value                  │
└──────────────────────────┘    │ unit                   │
                                 │ conditions             │
                                 │ source_id (FK, null)   │
                                 └────────────────────────┘
                                          │
                                          │ M:1
                                          ▼
                              ┌─────────────────────────┐
                              │    DataSource           │
                              ├─────────────────────────┤
                              │ id (PK)                 │
                              │ name                    │
                              │ description             │
                              │ url                     │
                              └─────────────────────────┘

┌──────────────────────────────┐
│      ImportLog               │
├──────────────────────────────┤
│ id (PK)                      │
│ imported_at (авто)           │
│ file_name                    │
│ total_rows                   │
│ success_count                │
│ error_count                  │
│ errors (JSON)                │
└──────────────────────────────┘
(не связана жёстко с другими таблицами)
```

## Таблица связей

| Таблица 1 | Связь | Таблица 2 | Комментарий |
|-----------|-------|----------|------------|
| Component | 1:M | ComponentAlias | Один компонент может иметь много синонимов |
| Component | 1:M | Property | Один компонент может иметь много свойств |
| DataSource | 1:M | Property | Один источник может быть указан для многих свойств |
| ImportLog | — | — | Независимая таблица, служит журналом импорта |

## Ключи

- **PK** (Primary Key) — первичный ключ, уникально идентифицирует запись
- **FK** (Foreign Key) — внешний ключ, ссылка на запись в другой таблице
- **M:1** (Many-to-One) — много записей связаны с одной (обратное отношение 1:M)
- **choices** — поле может содержать только предопределённые значения
- **null=True** — в БД может быть NULL (пусто)
- **auto_now_add=True** — автоматически заполняется текущей датой/временем при создании

## Пример данных

### Component
```
id=1, name="Water", formula="H2O", cas_number="7732-18-5", 
molar_mass=18.015, substance_class="Органическое", 
normal_boiling_point=100.0, ...
```

### ComponentAlias (для Component id=1)
```
id=1, component_id=1, alias_name="Вода", alias_type="ru"
id=2, component_id=1, alias_name="Aqua", alias_type="en"
id=3, component_id=1, alias_name="WATER", alias_type="aspen"
```

### Property (для Component id=1)
```
id=1, component_id=1, property_name="Плотность", 
value=1.0, unit="г/см³", conditions="20°C", source_id=1
```

### DataSource
```
id=1, name="NIST", description="Национальный институт стандартов", 
url="https://nist.gov"
```

### ImportLog
```
id=1, imported_at="2026-07-12 18:45:00", file_name="components.csv",
total_rows=30, success_count=28, error_count=2,
errors="[{row: 5, error: 'invalid molar_mass'}, ...]"
```
