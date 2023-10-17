from rest_framework import serializers

from datamaster import models


class DesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Desa
        lookup_field = "kode"
        fields = ["kode", "nama"]
