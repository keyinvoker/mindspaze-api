from flask import Blueprint
from flask_restful import Api

from mindspaze.resources.prediction import PredictionResource

prediction_bp = Blueprint("prediction_bp", __name__, url_prefix="")
prediction_api = Api(prediction_bp)
prediction_api.add_resource(PredictionResource, "/predict")
