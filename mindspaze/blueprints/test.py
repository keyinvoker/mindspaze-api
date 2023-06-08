from flask import Blueprint
from flask_restful import Api

from mindspaze.resources.test import TestResource

test_bp = Blueprint("test_bp", __name__, url_prefix="/test")
test_api = Api(test_bp)
test_api.add_resource(TestResource, "")
