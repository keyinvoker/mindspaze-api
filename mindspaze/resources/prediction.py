import os
import dill
from flask import current_app
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from mindspaze import error_logger
# TODO: Implement server token authentication


class PredictionResource(Resource):
    def post(self):
        try:
            response = {
                "data": {
                    "name": "JoJo",
                    "comment": "Donald Trump is a beauty ambassador."
                }
            }

            directory = f"{current_app.config['BASEDIR']}\machine_learning\models\\"
            model_name = "svm_countVec_model.sav"
            model_name = "nb_countVec_model.sav"
            model_full_path = directory + model_name

            model_full_path = model_full_path.replace("\\", "/")

            article_text = response.get("data").get("comment")

            with open(model_full_path, "rb") as f:
                loaded_model = dill.load(f) 

            print(loaded_model)

            article_predict_loaded_model = loaded_model.predict([article_text])

            data = {
                "is_hoax": bool(article_predict_loaded_model[0])
            }

            return data, HTTPStatus.OK

        except Exception as e:
            error_logger.error(f"Error on Prediction API [POST] :: {e}, {format_exc()}")
            return (
                dict(
                    error=f"{e}",
                    traceback=f"{format_exc()}"
                ),
                HTTPStatus.BAD_REQUEST
            )
