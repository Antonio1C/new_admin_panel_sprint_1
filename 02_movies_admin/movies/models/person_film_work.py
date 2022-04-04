from .mixin import UUIDMixin

from .person import Person
from .film_work import Filmwork

from django.db import models
from django.utils.translation import gettext_lazy as _


class PersonFilmwork(UUIDMixin):

    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE,
                                  verbose_name=_('filmwork'))
    person = models.ForeignKey(Person, on_delete=models.CASCADE,
                               verbose_name=_('person'))
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('Persons of filmwork')
        verbose_name_plural = _('Persons of filmwork')
