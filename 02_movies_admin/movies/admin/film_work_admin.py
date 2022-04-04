from django.contrib import admin
from ..models import Filmwork, GenreFilmwork, PersonFilmwork


class GenreFilmworkInLine(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInLine(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['person']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInLine, PersonFilmworkInLine)
    # Отображение полей в списке
    list_display = ['title', 'type', 'creation_date', 'rating',]

    # настройка фильтра
    list_filter = ('type',)

    # настройка полей поиска
    search_fields = ('title', 'description', 'id')
