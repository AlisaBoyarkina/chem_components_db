from django.contrib import admin
from .models import Component, ComponentAlias, Property,DataSource, ImportLog


admin.site.register(Component)
admin.site.register(ComponentAlias)
admin.site.register(Property)
admin.site.register(DataSource)
admin.site.register(ImportLog)
