import pickle

response = {
    "data": {
        "name": "JoJo",
        "comment": "Donald Trump is a beauty ambassador."
    }
}

# model_name = f"{os.getcwd()}\mindspaze\machine_learning\models\svm_countVec_model.sav"
model_name = "C:/Users/jojo/OneDrive/Email attachments/Dokumen/BackEnd/mindspaze-api/mindspaze/machine_learning/models/svm_countVec_model.sav"
model_name2 = "C:/Users/jojo/OneDrive/Email attachments/Dokumen/BackEnd/mindspaze-api/mindspaze/machine_learning/models/svm_countVec_model2.sav"

with open(model_name, "wb") as f:
    pickle.dump(model_name2, f, protocol=4)

with open(model_name2, "rb") as f:
    model = pickle.load(f)

article_text = response.get("data").get("comment")
article_predict_loaded_model = model.predict([article_text])

data = {
    "is_hoax": bool(article_predict_loaded_model[0])
}

print(data)