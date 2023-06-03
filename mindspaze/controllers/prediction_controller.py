import dill
import os
from sklearn.pipeline import Pipeline


class PredictionController:
    def __init__(self):
        _here = os.getcwd().replace('\\', '/')
        _directory = f"{_here}/machine_learning/models/"
        self.model_name = "svm_countVec_model.sav"
        self.model_name = "nb_countVec_model.sav"
        self.model_file_path = _directory + self.model_name

    def predict(self, text: str) -> bool:

        with open(self.model_file_path, "rb") as f:
            loaded_model: Pipeline = dill.load(f)

        article_predict_loaded_model = loaded_model.predict([text])
        is_hoax = bool(article_predict_loaded_model[0])

        return is_hoax
