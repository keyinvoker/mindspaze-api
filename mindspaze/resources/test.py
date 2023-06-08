from flask_restful import Resource
from http import HTTPStatus

from mindspaze.tools.response import make_json_response


class TestResource(Resource):
    def get(self):
        return make_json_response(
            http_status=HTTPStatus.OK,
            message="Test API for healthcheck",
            data=None,
        )
