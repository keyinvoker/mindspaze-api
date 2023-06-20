import json
from http import HTTPStatus
from flask import Response
from typing import Union

from mindspaze.schemas.response import (
    DefaultResponseSchema,
    DefaultStringResponseSchema,
)

default_messages = {status: status.name.replace("_", " ").title() for status in HTTPStatus}


def make_json_response(
    http_status: Union[HTTPStatus, int],
    data: dict = None,
    message="",
) -> Response:
    
    if not message and http_status in default_messages:
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
