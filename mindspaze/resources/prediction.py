from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from mindspaze import app_logger, error_logger
from mindspaze.controllers.prediction_controller import (
    PredictionController
)
from mindspaze.schemas.prediction import InputDataSchema
from mindspaze.tools.response import make_json_response


class PredictionResource(Resource):
    def post(self) -> Response:
        try:
            data_args = request.get_json()

            validation_error = InputDataSchema().validate(data_args)
            if validation_error:
                return make_json_response(
                    http_status=HTTPStatus.BAD_REQUEST,
                    message="Input data did not pass validation",
                    data=validation_error
                )

            payload = InputDataSchema().load(data_args)
            app_logger.info(f"Prediction [POST] :: payload: {payload}")

            article_text = payload.get("article_text")
            is_hoax = PredictionController().predict(article_text)

            data = dict(is_hoax=is_hoax)
            return make_json_response(
                http_status=HTTPStatus.OK,
                data=data
            )

        except Exception as e:
            error_logger.error(f"Error on Prediction [POST] :: {e}, {format_exc()}")
            return make_json_response(
                http_status=HTTPStatus.BAD_REQUEST,
                data=str(e)
            )
