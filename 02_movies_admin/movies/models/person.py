from .mixin import UUIDMixin, TimeStampedMixin

from django.db import models
from django.utils.translation import gettext_lazy as _

class Person(UUIDMixin, TimeStampedMixin):

    full_name = models.TextField(_('full_name'))

    class Meta:
        db_table = 'content"."person'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self) -> str:
        return self.full_name
