from flask import Blueprint
from flask_restful import Api

from mindspaze.resources.prediction import PredictionResource

mindspaze_bp = Blueprint("mindspaze_bp", __name__, url_prefix="/mindspaze")
mindspaze_api = Api(mindspaze_bp)

mindspaze_api.add_resource(PredictionResource, "/predict")
