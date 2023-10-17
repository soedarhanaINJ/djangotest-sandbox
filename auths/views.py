from auths import models, permissions, serializers
from core.views import LRCUViewSet


class UserViewSet(LRCUViewSet):
    queryset = models.User.objects.exclude(role=1).all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsSuperAdmin]

    ordering = ("-id",)
