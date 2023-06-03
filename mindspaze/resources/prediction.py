import json
from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from mindspaze import app_logger, error_logger
from mindspaze.controllers.prediction_controller import (
    PredictionController
)
from mindspaze.schemas.prediction import InputDataSchema


class PredictionResource(Resource):
    def post(self) -> Response:
        try:
            """
            TODO: needs coordination with FE
            response = {
                "data": {
                    "name": "JoJo",
                    "comment": "Donald Trump is a beauty ambassador."
                }
            }
            """
            data_args = request.get_json()

            validation_error = InputDataSchema().validate(data_args)
            if validation_error:
                return Response(
                    response=json.dumps(
                        {
                            "message": "Input data did not pass validation",
                            "data": dict(validation_error=validation_error)
                        }
                    ),
                    status=HTTPStatus.BAD_REQUEST,
                    mimetype="application/json"
                )

            payload = InputDataSchema().load(data_args)
            app_logger.info(f"Prediction [POST] :: payload: {payload}")

            article_text = payload.get("data").get("comment")  # TODO
            is_hoax = PredictionController().predict(article_text)

            data = dict(is_hoax=is_hoax)
            return Response(
                response=json.dumps(data),
                status=HTTPStatus.OK,
                mimetype="application/json"
            )

        except Exception as e:
            error_logger.error(f"Error on Prediction [POST] :: {e}, {format_exc()}")
            return Response(
                response=json.dumps(dict(error=str(e))),
                http_status=HTTPStatus.BAD_REQUEST,
                mimetype="application/json"
            )
