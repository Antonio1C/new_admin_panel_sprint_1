from django.contrib import admin
from ..models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']
