from typing import Any, TypeVar

from django.db import models
from django.db.models import JSONField, Model
from django.db.models.query import QuerySet

_MT = TypeVar("_MT", bound=Model)
_MT_co = TypeVar("_MT_co", bound=Model, covariant=True)
_QuerySetType = QuerySet[_MT_co]


def number_only_validator(value: str | int | None) -> None:
    if not value:
        return None

    value_str = str(value)
    return value_str.isdigit()


class LowerCharField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class BackgroundTask(models.Model):
    identifier = models.CharField(max_length=64, primary_key=True)
    task_id = models.CharField(max_length=32, unique=True)
    status = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "background_task"


class QueuedNotification(models.Model):
    payload = JSONField()
    is_read = models.BooleanField(default=False)
    receivers = models.ManyToManyField("auths.User")
    created_at = models.DateTimeField(auto_now_add=True)
