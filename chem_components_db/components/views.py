from django.shortcuts import render

from rest_framework import viewsets, filters
from .models import Component
from .serializers import ComponentListSerializer, ComponentDetailSerializer

class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    REST API для доступа к базе данных химических компонентов.
    Поддерживает поиск через query-параметр ?search=
    Пример: /api/v1/components/?search=METHANE
    """
    # Оптимизируем запросы к БД с помощью prefetch_related, чтобы избежать проблемы N+1
    queryset = Component.objects.all().prefetch_related('componentalias_set', 'property_set__source')
    filter_backends = [filters.SearchFilter]
    
    # Поля для поиска: название, формула, CAS и имена-синонимы (включая типы aspen/hysys)
    search_fields = ['name', 'formula', 'cas_number', 'componentalias__alias_name']

    def get_serializer_class(self):
        # Если запрашивается конкретный ID (карточка) — отдаем всё. Если список — облегченную версию.
        if self.action == 'retrieve':
            return ComponentDetailSerializer
        return ComponentListSerializer
