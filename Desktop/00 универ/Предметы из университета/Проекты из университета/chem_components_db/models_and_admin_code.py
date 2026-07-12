# ============================================================================
# components/models.py
# Модели базы данных химических компонентов
# ============================================================================

from django.db import models


class Component(models.Model):
    """
    Основная таблица с информацией о химических компонентах.
    Содержит физико-химические свойства вещества.
    """
    name = models.CharField(max_length=200, help_text="Название компонента (англ.)")
    formula = models.CharField(max_length=100, help_text="Химическая формула")
    cas_number = models.CharField(max_length=20, blank=True, help_text="CAS-номер (опционально)")
    molar_mass = models.FloatField(help_text="Молярная масса, г/моль")
    substance_class = models.CharField(max_length=100, blank=True, help_text="Класс вещества: спирт, углеводород и т.д.")
    normal_boiling_point = models.FloatField(null=True, blank=True, help_text="Температура кипения, °C")
    critical_temperature = models.FloatField(null=True, blank=True, help_text="Критическая температура, °C")
    critical_pressure = models.FloatField(null=True, blank=True, help_text="Критическое давление, атм")
    acentric_factor = models.FloatField(null=True, blank=True, help_text="Ацентрический фактор (безразмерный)")
    
    class Meta:
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненты"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.formula})"


class DataSource(models.Model):
    """
    Справочник источников данных.
    Используется для отслеживания происхождения информации о свойствах.
    """
    name = models.CharField(max_length=200, help_text="Название источника (NIST, справочник и т.д.)")
    description = models.TextField(blank=True, help_text="Описание источника")
    url = models.URLField(blank=True, help_text="Веб-адрес источника")
    
    class Meta:
        verbose_name = "Источник данных"
        verbose_name_plural = "Источники данных"
    
    def __str__(self):
        return self.name


class ComponentAlias(models.Model):
    """
    Синонимы / альтернативные названия компонентов.
    Один компонент может иметь несколько названий:
    - Русское (ru): "Вода"
    - Английское (en): "Water"
    - Aspen Plus (aspen): "WATER"
    - HYSYS (hysys): "WATER"
    
    Это необходимо для интеграции с разными системами (Aspen, HYSYS).
    """
    ALIAS_TYPES = [
        ('ru', 'Русское название'),
        ('en', 'English name'),
        ('aspen', 'Aspen Plus'),
        ('hysys', 'HYSYS'),
    ]
    
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='aliases')
    alias_name = models.CharField(max_length=200, help_text="Альтернативное название")
    alias_type = models.CharField(max_length=10, choices=ALIAS_TYPES, help_text="Тип названия")
    
    class Meta:
        verbose_name = "Синоним компонента"
        verbose_name_plural = "Синонимы компонентов"
        unique_together = ('component', 'alias_name', 'alias_type')
    
    def __str__(self):
        return f"{self.alias_name} ({self.component.name})"


class Property(models.Model):
    """
    Физико-химические свойства компонентов.
    Один компонент может иметь множество свойств:
    - Плотность при 20°C
    - Вязкость при 25°C
    - Теплоёмкость
    - и т.д.
    
    Каждое свойство может быть привязано к источнику данных (DataSource).
    """
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='properties')
    property_name = models.CharField(max_length=200, help_text="Название свойства: плотность, вязкость и т.д.")
    value = models.FloatField(help_text="Численное значение свойства")
    unit = models.CharField(max_length=50, help_text="Единица измерения: г/см³, cP, J/mol·K и т.д.")
    conditions = models.CharField(max_length=200, blank=True, help_text="Условия измерения: 20°C, 1 атм и т.д.")
    source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True, help_text="Источник данных")
    
    class Meta:
        verbose_name = "Свойство компонента"
        verbose_name_plural = "Свойства компонентов"
    
    def __str__(self):
        return f"{self.property_name}: {self.value} {self.unit} ({self.component.name})"


class ImportLog(models.Model):
    """
    Журнал импорта данных из CSV/Excel файлов.
    Используется Участником 3 для отслеживания:
    - Какие файлы были загружены
    - Сколько строк успешно добавлено
    - Какие ошибки возникли
    """
    imported_at = models.DateTimeField(auto_now_add=True, help_text="Время импорта (автоматическое)")
    file_name = models.CharField(max_length=200, help_text="Имя загруженного файла")
    total_rows = models.IntegerField(help_text="Всего строк в файле")
    success_count = models.IntegerField(help_text="Успешно загружено строк")
    error_count = models.IntegerField(help_text="Количество ошибок")
    errors = models.TextField(blank=True, help_text="JSON со списком ошибок по строкам")
    
    class Meta:
        verbose_name = "Журнал импорта"
        verbose_name_plural = "Журналы импорта"
        ordering = ['-imported_at']
    
    def __str__(self):
        return f"{self.file_name} ({self.imported_at.strftime('%Y-%m-%d %H:%M')})"


# ============================================================================
# components/admin.py
# Регистрация моделей в Django Admin
# ============================================================================

from django.contrib import admin
from .models import Component, ComponentAlias, Property, DataSource, ImportLog


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для компонентов.
    Позволяет просматривать, добавлять и редактировать компоненты.
    """
    list_display = ('name', 'formula', 'cas_number', 'molar_mass', 'substance_class')
    list_filter = ('substance_class',)
    search_fields = ('name', 'formula', 'cas_number')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'formula', 'cas_number', 'substance_class')
        }),
        ('Молярная масса', {
            'fields': ('molar_mass',)
        }),
        ('Критические параметры (опционально)', {
            'fields': ('critical_temperature', 'critical_pressure', 'acentric_factor'),
            'classes': ('collapse',)
        }),
        ('Температура кипения (опционально)', {
            'fields': ('normal_boiling_point',),
            'classes': ('collapse',)
        }),
    )


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для источников данных.
    """
    list_display = ('name', 'url')
    search_fields = ('name',)


@admin.register(ComponentAlias)
class ComponentAliasAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для синонимов компонентов.
    Показывает, к какому компоненту привязан каждый синоним.
    """
    list_display = ('alias_name', 'alias_type', 'component')
    list_filter = ('alias_type',)
    search_fields = ('alias_name', 'component__name')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для свойств компонентов.
    Позволяет просматривать и редактировать физико-химические данные.
    """
    list_display = ('property_name', 'component', 'value', 'unit', 'conditions')
    list_filter = ('property_name', 'component')
    search_fields = ('property_name', 'component__name')
    fieldsets = (
        ('Связь с компонентом', {
            'fields': ('component',)
        }),
        ('Свойство', {
            'fields': ('property_name', 'value', 'unit', 'conditions')
        }),
        ('Источник данных', {
            'fields': ('source',)
        }),
    )


@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для журнала импорта.
    Показывает историю загруженных файлов и результаты.
    """
    list_display = ('file_name', 'imported_at', 'total_rows', 'success_count', 'error_count')
    list_filter = ('imported_at',)
    search_fields = ('file_name',)
    readonly_fields = ('imported_at',)  # Нельзя менять время вручную
    fieldsets = (
        ('Информация о файле', {
            'fields': ('file_name', 'imported_at')
        }),
        ('Результаты импорта', {
            'fields': ('total_rows', 'success_count', 'error_count')
        }),
        ('Ошибки (JSON)', {
            'fields': ('errors',),
            'classes': ('collapse',)
        }),
    )
