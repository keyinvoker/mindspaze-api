import dill
import os
import requests
from flask import current_app
from http import HTTPStatus
from sklearn.pipeline import Pipeline
from typing import Dict, List, Optional, Union

from mindspaze import app_logger, error_logger
from mindspaze.helpers.prediction import clean_text
from mindspaze.tools.strings import remove_special_characters

TRUE_VALUES = [
    "mostly true",
    "true",
    "correct",
]

FALSE_VALUES = [
    "innacurate",
    "incorrect",
    "mostly false",
    "hoax",
    "misleading",
    "partly false",
    "keliru",
    "sesat",
    "falso",
    "faux",
    "false",
]


class PredictionController:
    def __init__(self):
        _here = os.getcwd().replace('\\', '/')
        if current_app.config.get("IS_LOCAL_SERVER"):
            _directory = f"{_here}/mindspaze/machine_learning/models/"
        else:
            _directory = f"{_here}/machine_learning/models/"

        self.model_name = "svm_countVec_model.sav"
        self.model_name = "nb_countVec_model.sav"
        self.model_file_path = _directory + self.model_name
        self.google_fact_checker_endpoint = current_app.config.get("GOOGLE_FACT_CHECKER_ENDPOINT")
        self.google_fact_checker_token = current_app.config.get("GOOGLE_FACT_CHECKER_TOKEN")

    def check_if_hoax(self, booleans: List[str]) -> bool:
        true_count = 0
        false_count = 0
        for boolean in booleans:
            segments = boolean.split()
            if any(segment in TRUE_VALUES for segment in segments):
                true_count += 1
            if any(segment in FALSE_VALUES for segment in segments):
                false_count += 1
        
        return true_count > false_count

    def predict_with_model(self, text: str) -> bool:
        with open(self.model_file_path, "rb") as f:
            loaded_model: Pipeline = dill.load(f)

        article_predict_loaded_model = loaded_model.predict([text])
        is_hoax = bool(article_predict_loaded_model[0])

        return is_hoax

    def predict_with_google(self, text: str) -> List[Optional[bool]]:
        text = clean_text(text)

        params = {
            "query": text,
            "key": self.google_fact_checker_token,
            "languageCode": "en-US",
        }

        response = requests.get(
            url=self.google_fact_checker_endpoint,
            params=params,
        )
        http_status = response.status_code
        payload = response.json()

        if http_status != HTTPStatus.OK or not payload:
            error_logger.error(f"predict_with_google() :: status: {http_status}, payload: {payload}")
            return []

        claims = response.json().get("claims")
        get_rating = lambda x: (
            remove_special_characters(
                x.get("claimReview")[0].get("textualRating").lower()
            )
        )

        ratings = list(map(get_rating, claims))
        ratings = self.check_if_hoax(ratings)
        return ratings

    def predict(self, text: str) -> Union[bool, List[None]]:
        model_rating = self.predict_with_model(text)

        google_rating = self.predict_with_google(text)

        return model_rating and google_rating
    
    def bulk_predict(self, payload: Dict[int, str]) -> Dict[int, bool]:
        result = dict()

        for id, text in payload.items():
            is_hoax: bool = self.predict(text)
            result[id] = is_hoax
            app_logger.info(f"bulk_predict() :: id: {id}, text: \"{text}\", is_hoax: {is_hoax}")

        return result
