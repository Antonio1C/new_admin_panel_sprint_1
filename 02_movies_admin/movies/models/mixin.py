import uuid

from django.db import models

class UUIDMixin(models.Model):
    # Типичная модель в Django использует число в качестве id.
    # В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(auto_now_add=True, null=True)

    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

