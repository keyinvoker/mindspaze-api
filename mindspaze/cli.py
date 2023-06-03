from flask.cli import AppGroup

from mindspaze.controllers.prediction_controller import PredictionController

prediction_cli = AppGroup("prediction", help="All CLIs related to MindSpaze")


@prediction_cli.command("all", help="Run prediction")
def predict_all():
    text = ""  # TODO: get from DB
    PredictionController().predict(text)
