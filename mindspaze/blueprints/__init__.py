from flask import Blueprint
from flask_restful import Api

from mindspaze.resources.banana import Banana

mindspaze_bp = Blueprint("mindspaze_bp", __name__, url_prefix="/mindspaze")
mindspaze_api = Api(mindspaze_bp)

mindspaze_api.add_resource(Banana, "/banana")
