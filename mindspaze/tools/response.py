import json
from http import HTTPStatus
from flask import Response
from typing import Optional, Union

from mindspaze.schemas.response import (
    DefaultResponseSchema,
    DefaultStringResponseSchema,
)

default_messages: dict = {
    status: status.name
    if status in [HTTPStatus.OK, HTTPStatus.IM_USED]
    else status.name.replace("_", " ").title()
    for status in HTTPStatus
}


def make_json_response(
    http_status: Union[HTTPStatus, int],
    data: Optional[dict] = None,
    message: str = "",
) -> Response:

    if not message:
        message = default_messages[http_status]

    if data:
        if data == {}:
            if len(data) > 0:
                response_data = DefaultResponseSchema().dump(
                    {"message": message, "code": http_status.value}
                )
                response_data["data"] = data
        else:
            response_data = DefaultStringResponseSchema().dump(
                {"message": message, "code": http_status.value, "data": data}
            )
    elif data == []:
        response_data = DefaultStringResponseSchema().dump(
            {"message": message, "code": http_status.value, "data": data}
        )
    else:
        response_data = DefaultResponseSchema().dump(
            {"message": message, "code": http_status.value, "data": data}
        )

    return Response(
        response=json.dumps(response_data),
        status=http_status,
        mimetype="application/json",
    )
