import pickle

from flask_restful import Resource


class PredictionResource(Resource):
    def post(self):
        # TODO: get data from MindSpaze web API

        model_name = "svm_countVec_model.sav"
        model_file = open(model_name, "wb")
        # pickle.dump(pipeline_svmCountVectorizer, model_file)
        model = pickle.load(model_file)

        # model.score(X_news_train, Y_label_train)

        article_text = "Carrier Still Moving Some Jobs to Mexico Despite Trump Deal"
        article_predict_loaded_model = model.predict([article_text])

        data = {
            "is_not_hoax": article_predict_loaded_model
        }

        return data, 200
