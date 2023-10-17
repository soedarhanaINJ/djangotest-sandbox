from typing import Any, Dict, List, Optional, Union

from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exc_handler(exc: Exception, context: Any) -> Optional[Response]:
    response = exception_handler(exc, context)
    if response is not None:
        data: Dict[str, Union[List[str], dict]] = {}
        if "detail" in response.data:
            detail = response.data.get("detail")
            if isinstance(detail, list):
                data["errors"] = detail
            else:
                data["errors"] = [detail]
        else:
            detail = response.data
            if isinstance(detail, list):
                data["errors"] = detail
            elif isinstance(detail, dict):
                data["errors"] = detail
            else:
                data["errors"] = [detail]

        response.data = data
    return response
