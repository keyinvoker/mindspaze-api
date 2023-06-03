import json
import os
import dill
from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from mindspaze import app_logger, error_logger
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

            here = os.getcwd().replace("\\", "/")
            directory = f"{here}/machine_learning/models"
            model_name = "svm_countVec_model.sav"
            model_name = "nb_countVec_model.sav"
            model_full_path = directory + model_name

            article_text = payload.get("data").get("comment")  # TODO

            with open(model_full_path, "rb") as f:
                loaded_model = dill.load(f)

            article_predict_loaded_model = loaded_model.predict([article_text])

            data = {
                "is_hoax": bool(article_predict_loaded_model[0])
            }

            return Response(
                response=json.dumps(data),
                status=HTTPStatus.OK,
                mimetype="application/json"
            )

        except Exception as e:
            error_logger.error(
                f"Error on Prediction [POST] :: {e}, {format_exc()}")
            return (
                dict(
                    error=f"{e}",
                    traceback=f"{format_exc()}"
                ),
                HTTPStatus.BAD_REQUEST
            )
