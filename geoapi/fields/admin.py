from django.contrib import admin
from .models import Field

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'crop', 'area_ha', 'region', 'geometry')
    search_fields = ['crop', 'region']
