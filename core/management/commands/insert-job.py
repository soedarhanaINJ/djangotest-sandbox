from typing import Any

from django.core.management.base import BaseCommand
from django_q.tasks import Schedule


class Command(BaseCommand):
    help = "Insert scheduled task"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        defaults = {"schedule_type": Schedule.CRON, "cron": "0 0 * * *"}
        Schedule.objects.update_or_create(
            func="plotmanagement.tasks.update_status_perpanjangan",
            defaults=defaults,
        )
        print("Perpanjangan status scheduled.")
