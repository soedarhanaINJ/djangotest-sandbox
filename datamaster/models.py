from django.db import models
from safedelete.models import NO_DELETE, SafeDeleteModel


class Desa(SafeDeleteModel):
    _safedelete_policy = NO_DELETE

    kode = models.CharField(max_length=10)
    nama = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.nama

    class Meta:
        db_table = "desa"
