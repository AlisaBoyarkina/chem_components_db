from rest_framework import serializers
from .models import Component, ComponentAlias, Property, DataSource

class ComponentAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentAlias
        fields = ['id', 'alias_name', 'alias_type']  # ru, en, aspen, hysys

class PropertySerializer(serializers.ModelSerializer):
    # Выводим текстовое название источника вместо его ID
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'property_name', 'value', 'unit', 'conditions', 'source_name']

class ComponentListSerializer(serializers.ModelSerializer):
    """Краткая информация для списка веществ"""
    class Meta:
        model = Component
        fields = ['id', 'name', 'formula', 'cas_number', 'molar_mass', 'substance_class']

class ComponentDetailSerializer(serializers.ModelSerializer):
    """Полная карточка со всеми константами, свойствами и синонимами Aspen/HYSYS"""
    aliases = ComponentAliasSerializer(many=True, read_only=True, source='componentalias_set')
    properties = PropertySerializer(many=True, read_only=True, source='property_set')

    class Meta:
        model = Component
        fields = [
            'id', 'name', 'formula', 'cas_number', 'molar_mass', 'substance_class',
            'normal_boiling_point', 'critical_temperature', 'critical_pressure', 'acentric_factor',
            'aliases', 'properties'
        ]