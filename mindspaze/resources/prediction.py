from http import HTTPStatus
import pickle
import os
from traceback import format_exc

from flask_restful import Resource


class PredictionResource(Resource):
    def post(self):
        try:
            response = {
                "data": {
                    "name": "JoJo",
                    "comment": "Donald Trump is a beauty ambassador."
                }
            }

            # model_name = f"{os.getcwd()}\mindspaze\machine_learning\models\svm_countVec_model.sav"
            model_name = "C:/Users/jojo/OneDrive/Email attachments/Dokumen/BackEnd/mindspaze-api/mindspaze/resources/prediction.py"

            with open(model_name, "rb") as model_file:
                model = pickle.load(model_file)
    
            article_text = response.get("data").get("comment")
            article_predict_loaded_model = model.predict([article_text])

            data = {
                "is_hoax": bool(article_predict_loaded_model[0])
            }

            return data, HTTPStatus.OK
            return article_text, HTTPStatus.OK
        except Exception as e:
            return (
                dict(
                    error=f"Error :: {e}",
                    traceback=f"{format_exc()}"
                ),
                HTTPStatus.BAD_REQUEST
            )
