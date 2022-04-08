from .mixin import UUIDMixin

from .genre import Genre
from .film_work import Filmwork

from django.db import models
from django.utils.translation import gettext_lazy as _


class GenreFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE,
                                  verbose_name=_('filmwork'))
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('Genres of filmwork')
        verbose_name_plural = _('Genres of filmwork')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'genre_id'],
                name='genre_film_work_film_work_id_genre_id_uniq'
            )
        ]
