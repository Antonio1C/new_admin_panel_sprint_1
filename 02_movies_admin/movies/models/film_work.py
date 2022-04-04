from .mixin import UUIDMixin, TimeStampedMixin
from .genre import Genre
from .person import Person

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Types(models.TextChoices):
        MOVIE = _('movie')
        TV_SHOW = _('tv show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(10)], null=True)
    type = models.CharField(_('type'), choices=Types.choices,
                            default=Types.MOVIE,
                            max_length=7)

    # file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        # указываем, что таблица находится в нестандартной схеме
        db_table = 'content"."film_work'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')

    def __str__(self) -> str:
        return self.title

