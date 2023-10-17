from core.filters import COMPLETE_FILTER
from core.views import LRViewSet

from datamaster import models, serializers


class DesaViewSet(LRViewSet):
    queryset = models.Desa.objects.order_by("kode")
    serializer_class = serializers.DesaSerializer

    filter_backends = COMPLETE_FILTER
    search_fields = ["nama"]
