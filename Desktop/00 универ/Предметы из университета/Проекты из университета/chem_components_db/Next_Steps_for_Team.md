# План действий для остальных участников команды

Участник 1 (Алиса) завершила проектирование и создание структуры БД. Дальше работают Участники 2-5.

---

## Участник 2: Web-интерфейс (просмотр и поиск)

### Что уже есть
- ✅ Модели в `components/models.py` (Component, ComponentAlias, Property, DataSource)
- ✅ Админ-панель для ввода данных в `components/admin.py`
- ✅ БД создана и готова

### Что нужно сделать

**1. Создать views (функции для отображения данных)**

Файл: `components/views.py`

```python
from django.shortcuts import render, get_object_or_404
from .models import Component

def component_list(request):
    """Список всех компонентов"""
    components = Component.objects.all()
    return render(request, 'components/list.html', {'components': components})

def component_detail(request, pk):
    """Карточка одного компонента со всеми свойствами и синонимами"""
    component = get_object_or_404(Component, pk=pk)
    return render(request, 'components/detail.html', {'component': component})
```

**2. Создать HTML-шаблоны**

Файл: `components/templates/components/list.html`
- Таблица всех компонентов
- Колонки: название, формула, молярная масса
- Ссылка на карточку компонента

Файл: `components/templates/components/detail.html`
- Все данные компонента
- Список синонимов (aliases)
- Список свойств (properties)

**3. Добавить маршруты в `components/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.component_list, name='list'),
    path('<int:pk>/', views.component_detail, name='detail'),
]
```

**4. Подключить в главном `config/urls.py`**

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('components/', include('components.urls')),
]
```

**5. Добавить поиск**

- Форма поиска в list.html
- Фильтр по названию, формуле, CAS-номеру
- Использовать `__icontains` для нечувствительного к регистру поиска

```python
# в views.py
from django.db.models import Q

def component_list(request):
    search = request.GET.get('q', '')
    components = Component.objects.all()
    if search:
        components = components.filter(
            Q(name__icontains=search) | 
            Q(formula__icontains=search) |
            Q(cas_number__icontains=search)
        )
    return render(request, 'components/list.html', {'components': components, 'search': search})
```

### На защите показать:
- Список компонентов на сайте
- Поиск по названию/формуле
- Клик на компонент → открывается карточка со свойствами и синонимами

---

## Участник 3: Импорт данных (CSV/Excel)

### Что уже есть
- ✅ Модели Component и Property готовы
- ✅ Модель ImportLog для логирования

### Что нужно сделать

**1. Создать форму загрузки файла**

Файл: `components/forms.py`

```python
from django import forms

class ComponentImportForm(forms.Form):
    file = forms.FileField(
        help_text="Поддерживаются CSV и Excel (.xlsx, .xls)",
        widget=forms.FileInput(attrs={'accept': '.csv,.xlsx,.xls'})
    )
```

**2. Написать парсер**

Файл: `components/importers.py`

```python
import csv
from .models import Component, Property, DataSource, ImportLog

def import_csv(file_path):
    """Парсит CSV и загружает в БД"""
    total_rows = 0
    success_count = 0
    error_count = 0
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Ожидаемые столбцы: name, formula, cas_number, molar_mass
            for row_num, row in enumerate(reader, start=1):
                total_rows += 1
                try:
                    # Валидация обязательных полей
                    if not row.get('name') or not row.get('formula'):
                        raise ValueError("Missing required fields")
                    
                    # Создание компонента
                    component, created = Component.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'formula': row['formula'],
                            'cas_number': row.get('cas_number', ''),
                            'molar_mass': float(row.get('molar_mass', 0)),
                        }
                    )
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append({
                        'row': row_num,
                        'error': str(e),
                        'data': row
                    })
        
        # Логирование результата
        import_log = ImportLog.objects.create(
            file_name=file_path,
            total_rows=total_rows,
            success_count=success_count,
            error_count=error_count,
            errors=str(errors)
        )
        
        return import_log
    
    except Exception as e:
        print(f"Import error: {e}")
        return None
```

**3. Создать view для загрузки**

```python
# в components/views.py
from django.shortcuts import render
from .forms import ComponentImportForm
from .importers import import_csv

def import_components(request):
    if request.method == 'POST':
        form = ComponentImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Сохрани временный файл и парсь его
            result = import_csv(file)
            return render(request, 'components/import_result.html', {'result': result})
    else:
        form = ComponentImportForm()
    return render(request, 'components/import.html', {'form': form})
```

**4. Шаблон результата импорта**

Файл: `components/templates/components/import_result.html`
- Показать: всего загружено, успешно, ошибок
- Список ошибок (если были)

### Данные для тестирования

Создай `data/demo_components.csv`:
```
name,formula,cas_number,molar_mass,substance_class
Water,H2O,7732-18-5,18.015,Inorganic
Ethanol,C2H6O,64-17-5,46.07,Organic Alcohol
Methane,CH4,74-82-8,16.043,Hydrocarbon
Propane,C3H8,74-98-6,44.096,Hydrocarbon
...
```

### На защите показать:
- Форма загрузки CSV
- Успешная загрузка (30 компонентов)
- Отображение результата (X загружено, Y ошибок)
- Данные появились в админ-панели и на сайте

---

## Участник 4: REST API

### Что уже есть
- ✅ Модели готовы
- ✅ Данные будут в БД (после импорта Участника 3)

### Что нужно сделать

**1. Установить Django REST Framework**

```bash
pip install djangorestframework
```

Добавить в `config/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'components',
]
```

**2. Создать сериализаторы**

Файл: `components/serializers.py`

```python
from rest_framework import serializers
from .models import Component, ComponentAlias, Property

class ComponentAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentAlias
        fields = ['alias_name', 'alias_type']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['property_name', 'value', 'unit', 'conditions']

class ComponentSerializer(serializers.ModelSerializer):
    aliases = ComponentAliasSerializer(many=True, read_only=True)
    properties = PropertySerializer(many=True, read_only=True)
    
    class Meta:
        model = Component
        fields = ['id', 'name', 'formula', 'cas_number', 'molar_mass', 
                  'substance_class', 'aliases', 'properties']
```

**3. Создать API views**

Файл: `components/api_views.py`

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Component, ComponentAlias
from .serializers import ComponentSerializer

@api_view(['GET'])
def search_component(request):
    """
    Поиск компонента по названию, CAS-номеру или формуле
    GET /api/components/search/?name=WATER
    """
    name = request.query_params.get('name', '').upper()
    
    if not name:
        return Response({
            'query': name,
            'matched': False,
            'error': 'Parameter "name" is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Поиск в синонимах
    alias = ComponentAlias.objects.filter(
        Q(alias_name__iexact=name) | 
        Q(component__name__iexact=name)
    ).first()
    
    if alias:
        component = alias.component
        serializer = ComponentSerializer(component)
        return Response({
            'query': name,
            'matched': True,
            'component': serializer.data
        })
    
    # Поиск в основной таблице
    component = Component.objects.filter(
        Q(name__iexact=name) | 
        Q(formula__iexact=name) |
        Q(cas_number__iexact=name)
    ).first()
    
    if component:
        serializer = ComponentSerializer(component)
        return Response({
            'query': name,
            'matched': True,
            'component': serializer.data
        })
    
    return Response({
        'query': name,
        'matched': False,
        'component': None
    })

@api_view(['GET'])
def component_list(request):
    """Получить список всех компонентов"""
    components = Component.objects.all()
    serializer = ComponentSerializer(components, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def component_detail(request, pk):
    """Получить данные одного компонента по ID"""
    try:
        component = Component.objects.get(pk=pk)
        serializer = ComponentSerializer(component)
        return Response(serializer.data)
    except Component.DoesNotExist:
        return Response({'error': 'Component not found'}, status=status.HTTP_404_NOT_FOUND)
```

**4. Подключить маршруты**

Файл: `components/api_urls.py`

```python
from django.urls import path
from . import api_views

urlpatterns = [
    path('search/', api_views.search_component, name='api-search'),
    path('list/', api_views.component_list, name='api-list'),
    path('<int:pk>/', api_views.component_detail, name='api-detail'),
]
```

В `config/urls.py`:
```python
urlpatterns = [
    ...
    path('api/components/', include('components.api_urls')),
]
```

### Примеры запросов (для документации)

```
GET /api/components/search/?name=WATER
{
    "query": "WATER",
    "matched": true,
    "component": {
        "id": 1,
        "name": "Water",
        "formula": "H2O",
        "cas_number": "7732-18-5",
        "molar_mass": 18.015,
        "substance_class": "Inorganic",
        "aliases": [
            {"alias_name": "Вода", "alias_type": "ru"},
            {"alias_name": "Water", "alias_type": "en"}
        ],
        "properties": [...]
    }
}
```

### На защите показать:
- Запрос в Postman/браузер: /api/components/search/?name=WATER
- JSON-ответ с компонентом
- Договорённость со второй командой о формате API

---

## Участник 5: Тестирование и документация

### Что нужно сделать

**1. Написать unit-тесты**

Файл: `components/tests/test_models.py`

```python
from django.test import TestCase
from components.models import Component, ComponentAlias

class ComponentTestCase(TestCase):
    def setUp(self):
        self.component = Component.objects.create(
            name="Water",
            formula="H2O",
            molar_mass=18.015
        )
    
    def test_component_creation(self):
        self.assertEqual(self.component.name, "Water")
    
    def test_component_str(self):
        self.assertEqual(str(self.component), "Water (H2O)")
    
    def test_component_alias_creation(self):
        alias = ComponentAlias.objects.create(
            component=self.component,
            alias_name="Вода",
            alias_type="ru"
        )
        self.assertIn(alias, self.component.aliases.all())
```

**2. Запустить тесты**

```bash
python3 manage.py test components
```

**3. Доделать README.md**

- Инструкция запуска
- Описание всех таблиц
- Примеры использования
- Решение типичных проблем

**4. Создать api_examples.md**

Примеры всех запросов API с результатами (для второй команды).

**5. Подготовить демонстрационный сценарий**

На защите:
1. Показать проект на GitHub/в файлах
2. Запустить сервер: `python3 manage.py runserver`
3. Открыть админ-панель: список компонентов
4. Открыть веб-сайт: поиск компонента
5. Показать API: запрос к /api/components/search/?name=WATER
6. Рассказ каждого участника (2-3 мин)

---

## Интеграция со второй командой (Aspen Plus / HYSYS)

Вторая команда будет:
1. Получать данные из Aspen/HYSYS расчётной схемы
2. Искать компоненты через API: `/api/components/search/?name=WATER`
3. Получать JSON-ответ с данными из нашей БД
4. Сравнивать и использовать для расчётов

**Критичные моменты:**
- API должен быть быстрым (закэшировать часто запрашиваемые)
- Названия полей в JSON должны быть зафиксированы и согласованы
- Второй команде нужна документация примеров запросов (api_examples.md)

---

## Сроки (примерно)

| День | Что делать |
|------|-----------|
| **1-2** | Все участники читают README, обсуждают архитектуру, согласуют API |
| **2-3** | Участник 2 делает веб-интерфейс, Участник 3 пишет парсер |
| **3-4** | Участник 4 делает API, Участник 5 готовит тесты и README |
| **4-5** | Интеграция, тестирование, исправление багов |
| **6-7** | Финальный прогон сценария защиты, оформление отчётов |

---

## Контрольный список перед защитой

- [ ] БД создана (✅ Участник 1)
- [ ] Веб-интерфейс работает (список, карточка, поиск)
- [ ] CSV импорт работает (загрузка файла, логирование)
- [ ] REST API работает (поиск, JSON-ответы)
- [ ] Тесты написаны и проходят
- [ ] README полный и актуальный
- [ ] API примеры для второй команды (api_examples.md)
- [ ] Демонстрационный датасет загружен (30+ компонентов)
- [ ] Сценарий защиты прописан и отрепетирован

---

## Вопросы к Участнику 1 (Алиса) во время защиты

- Почему выбрали именно такую структуру БД?
- Как связаны Component и ComponentAlias?
- Зачем нужна таблица ImportLog?
- Как система обрабатывает удаление компонента?
- Какие поля обязательные, какие опциональные и почему?

**Ответы (для подготовки):**
- Структура соответствует требованиям методички и обеспечивает все необходимые связи
- ComponentAlias позволяет искать компонент по названию в разных системах (Aspen, HYSYS, русском, английском)
- ImportLog логирует результаты загрузки для отслеживания ошибок
- Если удалить компонент (CASCADE) — удалятся синонимы и свойства
- Обязательные: поля, без которых компонент не имеет смысла (name, formula, molar_mass); опциональные: дополнительные параметры (свойства), которых может не быть

---

✅ **Все готово! Начинайте работу.**
