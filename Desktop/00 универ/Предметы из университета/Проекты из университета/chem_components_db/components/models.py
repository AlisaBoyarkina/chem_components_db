from django.db import models

class Component(models.Model):
    name = models.CharField(max_length=200)
    formula = models.CharField(max_length=200)
    cas_number = models.CharField(max_length=20, blank=True)
    molar_mass = models.FloatField()
    substance_class = models.CharField(max_length=100, blank=True)
    normal_boiling_point = models.FloatField(null=True, blank=True)
    critical_temperature = models.FloatField(null=True, blank=True)
    critical_pressure = models.FloatField(null=True, blank=True)
    acentric_factor = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class DataSource(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class ComponentAlias(models.Model):
    ALIAS_TYPES = [
        ('ru', 'Русское название'),
        ('en', 'English name'),
        ('aspen', 'Aspen Plus'),
        ('hysys', 'HYSYS'),
    ]
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='aliases')
    alias_name = models.CharField(max_length=200)
    alias_type = models.CharField(max_length=10, choices=ALIAS_TYPES)

    def __str__(self):
        return f"{self.alias_name} ({self.component.name})"


class Property(models.Model):
    component =models.ForeignKey(Component, on_delete=models.CASCADE, related_name='properties')
    property_name = models.CharField(max_length=200)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    conditions = models.CharField(max_length=200,blank=True)
    source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.property_name} ({self.component.name})"


class ImportLog(models.Model):
    imported_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=200)
    total_rows = models.IntegerField()
    success_count = models.IntegerField()
    error_count = models.IntegerField()
    errors = models.TextField(blank=True)
    
    def __str__(self):
            return f"{self.file_name} ({self.imported_at})"
        









    
    
