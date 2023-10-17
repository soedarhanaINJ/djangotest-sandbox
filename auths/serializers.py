from rest_framework import serializers

from auths import models
from datamaster.models import Desa
from datamaster.serializers import DesaSerializer


class UserSerializer(serializers.ModelSerializer):
    desa = serializers.SlugRelatedField(
        slug_field="kode", queryset=Desa.objects.all()
    )
    desa_data = DesaSerializer(source="desa", read_only=True)

    def create(self, validated_data: dict) -> models.User:
        password = validated_data.get("password")
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()

        return instance

    def update(
        self, instance: models.User, validated_data: dict
    ) -> models.User:
        password = validated_data.get("password")
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = models.User
        fields = [
            "id",
            "desa",
            "desa_data",
            "username",
            "email",
            "password",
            "role",
        ]
