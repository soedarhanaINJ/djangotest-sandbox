import json
from decimal import Decimal
from typing import Any

from rest_framework import fields
from rest_framework.serializers import ModelSerializer, Serializer

from core import models


class FileUploadSerializer(Serializer):
    file = fields.FileField(required=True)


class MsgRespondSerializer(Serializer):
    msg = fields.CharField(required=True)


class UrlRespondSerializer(Serializer):
    msg = fields.CharField(required=True)


class QIdentifierSerializer(Serializer):
    identifier = fields.CharField(required=True)


class QStatusSerializer(Serializer):
    status = fields.CharField()
    total_data = fields.IntegerField()
    data_processed = fields.IntegerField()
    data_failed = fields.IntegerField()
    data_success = fields.IntegerField()


class QueuedNotificationSerializer(ModelSerializer):
    class Meta:
        model = models.QueuedNotification
        fields = ["id", "payload"]


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
