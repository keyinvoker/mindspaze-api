import pickle

response = {
    "data": {
        "name": "JoJo",
        "comment": "Donald Trump is a beauty ambassador."
    }
}

# model_name = f"{os.getcwd()}\mindspaze\machine_learning\models\svm_countVec_model.sav"
model_name = "C:/Users/jojo/OneDrive/Email attachments/Dokumen/BackEnd/mindspaze-api/mindspaze/resources/prediction.py"

with open(model_name, "rb") as f:
    model = pickle.dump(mdf)

with open(model_name, "rb") as f:
    model = pickle.load(f)

article_text = response.get("data").get("comment")
article_predict_loaded_model = model.predict([article_text])

data = {
    "is_hoax": bool(article_predict_loaded_model[0])
}

print(data)
