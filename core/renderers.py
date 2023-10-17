from typing import Any, Optional

from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Any] = None,
    ) -> bytes:
        if data is None:
            return b""

        checked_keys = ("meta", "errors", "data")
        if not any(i in data for i in checked_keys):
            data = {"data": data}
        return super().render(data, accepted_media_type, renderer_context)
