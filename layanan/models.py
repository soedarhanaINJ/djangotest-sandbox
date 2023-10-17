from typing import Optional

from django.db import models
from safedelete.models import HARD_DELETE, SafeDeleteModel

LAYANAN_STATUS_CHOICES = (
    ("received", "Diterima"),
    ("accepted", "Disetujui oleh Kepala Bagian"),
    ("rejected", "Ditolak oleh Kepala Bagian"),
    ("correction", "Diperbaiki oleh Penduduk"),
    ("approved", "Disetujui oleh Kepala Desa"),
    ("success", "Dicetak"),
)

LAYANAN_TYPE_CHOICES = (
    ("pemerintahan", "Layanan Pemerintahan"),
    ("umum", "Layanan Umum"),
)


class LayananHistory(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE

    desa = models.ForeignKey("datamaster.Desa", on_delete=models.CASCADE)
    obj_id = models.BigIntegerField()
    obj_type = models.CharField(choices=LAYANAN_TYPE_CHOICES, max_length=16)
    status = models.CharField(choices=LAYANAN_STATUS_CHOICES, max_length=16)
    rejection_reason = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "auths.User",
        on_delete=models.CASCADE,
        related_name="layanan_history_created",
    )
    updated_by = models.ForeignKey(
        "auths.User",
        on_delete=models.CASCADE,
        related_name="layanan_history_updated",
    )

    class Meta:
        db_table = "layanan_history"


class LayananHistoryDetail(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE

    parent = models.ForeignKey(LayananHistory, on_delete=models.CASCADE)
    status = models.CharField(choices=LAYANAN_STATUS_CHOICES, max_length=16)
    rejection_reason = models.TextField(null=True)
    actor = models.ForeignKey(
        "auths.User",
        on_delete=models.CASCADE,
        related_name="history_detail_actor",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "layanan_history_detail"


class LayananBaseModel(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE
    tipe: str

    desa = models.ForeignKey("datamaster.Desa", on_delete=models.CASCADE)
    keperluan = models.CharField(max_length=32)
    keterangan = models.CharField(max_length=32)
    status = models.CharField(choices=LAYANAN_STATUS_CHOICES, max_length=16)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "auths.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        "auths.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_updated",
    )

    def get_history(self) -> Optional[LayananHistory]:
        return LayananHistory.objects.filter(
            obj_id=self.pk, obj_type=self.tipe
        ).first()

    class Meta:
        abstract = True


class LayananPemerintahan(LayananBaseModel):
    tipe = "pemerintahan"

    class Meta:
        db_table = "layanan_pemerintahan"


class LayananUmum(LayananBaseModel):
    tipe = "umum"

    class Meta:
        db_table = "layanan_umum"
