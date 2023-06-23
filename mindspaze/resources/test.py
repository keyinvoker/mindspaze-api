from flask import request
from flask_restful import Resource
from http import HTTPStatus

from mindspaze.tools.response import make_json_response


class TestResource(Resource):
    def get(self):
        payload = request.args.to_dict()

        return make_json_response(
            http_status=HTTPStatus.OK,
            message="Test API for healthcheck",
            data=payload,
        )
