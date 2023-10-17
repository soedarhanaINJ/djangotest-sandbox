from collections import OrderedDict
from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = "per_page"

    def get_paginated_response(self, data: Any) -> Response:
        if self.page is None:
            raise AttributeError("No page attribute found.")
        if self.request is None:
            raise AttributeError("No request attribute found.")

        meta = OrderedDict(
            [
                ("page", self.page.number),
                ("total", self.page.paginator.count),
                ("per_page", self.get_page_size(self.request)),
                ("total_page", self.page.paginator.num_pages),
            ]
        )

        return Response(OrderedDict([("meta", meta), ("data", data)]))

    def get_paginated_response_schema(self, schema: Any) -> dict:
        return {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "per_page": {"type": "integer", "example": 10},
                        "total": {"type": "integer", "example": 100},
                        "total_page": {"type": "integer", "example": 10},
                    },
                },
                "data": schema,
            },
        }
