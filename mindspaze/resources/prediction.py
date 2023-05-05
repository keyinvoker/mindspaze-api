import pickle
import joblib
import os
from http import HTTPStatus
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

            # here = os.path.abspath(os.path.dirname(__file__))

            # model_name = f"{os.getcwd()}\mindspaze\machine_learning\models\svm_countVec_model.sav"
            model_directory = "C:/Users/jojo/OneDrive/Email attachments/Dokumen/BackEnd/mindspaze-api/mindspaze/machine_learning/models/"
            model_name = "svm_countVec_model.sav"
            model_name = "nb_countVec_model.sav"
            model_full_path = model_directory + model_name
    
            article_text = response.get("data").get("comment")
            loaded_model = joblib.load(model_full_path)
            article_predict_loaded_model = loaded_model.predict([article_text])

            data = {
                "is_hoax": bool(article_predict_loaded_model[0])
            }

            return data, HTTPStatus.OK

        except Exception as e:
            return (
                dict(
                    error=f"Error :: {e}",
                    traceback=f"{format_exc()}"
                ),
                HTTPStatus.BAD_REQUEST
            )
