from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork

# Register your models here.


class GenreFilmworkInLine(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInLine(admin.TabularInline):
    model = PersonFilmwork
    raw_id_fields = ('person',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInLine, PersonFilmworkInLine)
    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)

    # настройка фильтра
    list_filter = ('type',)

    # настройка полей поиска
    search_fields = ('title', 'description', 'id')
