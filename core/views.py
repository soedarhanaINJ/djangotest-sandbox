from typing import Any, Dict, Optional, Type, Union

from django.db.models import Model
from django.db.models.fields.reverse_related import ManyToOneRel, OneToOneRel
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (BaseSerializer, ModelSerializer,
                                        Serializer)
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from core import serializers
from core.models import BackgroundTask
from core.utils import compose_words


class CustomGenericViewSet(GenericViewSet):
    detail_serializer_class: Optional[Type[ModelSerializer]] = None
    action_serializer: Dict[
        str, Union[Type[ModelSerializer], Type[Serializer]]
    ] = {}

    def get_serializer_class(
        self,
    ) -> Union[Type[ModelSerializer], Type[Serializer], Type[BaseSerializer]]:
        detail_action = ("create", "retrieve", "update", "partial_update")
        if (
            self.detail_serializer_class is not None
            and self.action in detail_action
        ):
            return self.detail_serializer_class

        return super().get_serializer_class()


class CustomDestroyMixin:
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()  # type:ignore
        instance_class = type(instance)
        fields_map = instance_class._meta.fields_map
        print(fields_map)

        used_in = []
        for rel_name, rel_instance in fields_map.items():
            print(rel_name)
            if "+" in rel_name:
                continue
            has_relation = False
            if isinstance(rel_instance, OneToOneRel):
                if getattr(instance, rel_name, None):
                    has_relation = True
            else:
                query_key = ""
                if rel_instance.related_name:
                    query_key = rel_instance.related_name
                else:
                    query_key = rel_name + "_set"

                if getattr(instance, query_key).exists():
                    has_relation = True

            if has_relation:
                rel_human_name = getattr(
                    rel_instance.related_model, "_human_name", rel_name
                )
                used_in.append(rel_human_name)

        if used_in:
            warning_text = compose_words(used_in)
            raise ValidationError(
                f"Data ini masih terpakai pada {warning_text}"
            )

        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance: Model) -> None:
        instance.delete()


class LViewSet(CustomGenericViewSet, ListModelMixin):
    pass


class LRViewSet(CustomGenericViewSet, ListModelMixin, RetrieveModelMixin):
    pass


class LCViewSet(CustomGenericViewSet, CreateModelMixin, ListModelMixin):
    pass


class LRCUViewSet(
    CustomGenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
):
    pass


class CompleteViewSet(
    CustomGenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    CustomDestroyMixin,
):
    pass


class LRUViewSet(
    CustomGenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    pass


class QStatusView(APIView):
    serializer_class = serializers.QStatusSerializer

    def get(self, request: Request, identifier: str) -> Response:
        instance = BackgroundTask.objects.filter(identifier=identifier).first()
        if not instance:
            raise NotFound()

        status = instance.status
        if "file" in status:
            status["file"] = request.build_absolute_uri(status["file"])

        return Response({"data": status})
