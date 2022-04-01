import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UUIDMixin(models.Model):
    # Типичная модель в Django использует число в качестве id.
    # В таких ситуациях поле не описывается в модели.
    # Нам же придётся явно объявить primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(auto_now_add=True)

    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_('name'), max_length=255)

    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме.
        # Это нужно указать в классе модели
        db_table = 'content"."genre'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self) -> str:
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Types(models.TextChoices):
        MOVIE = _('movie')
        TV_SHOW = _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), choices=Types.choices,
                            default=Types.MOVIE,
                            max_length=7)

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        # указываем, что таблица находится в нестандартной схеме
        db_table = 'content"."film_work'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')

    def __str__(self) -> str:
        return self.title


class GenreFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'


class Person(UUIDMixin, TimeStampedMixin):

    full_name = models.TextField(_('full_name'))

    class Meta:
        db_table = 'content"."person'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self) -> str:
        return self.full_name


class PersonFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
