from keras.models import model_from_json
from keras.preprocessing import sequence
import numpy as np

search_model_word_table = {}

with open('./Deeplearning_Model/word_table.txt', 'r') as js:
    text = js.read()
    search_model_word_table = eval(text)

json_file = open("./Deeplearning_Model/model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("./Deeplearning_Model/model.h5")
print("Loaded search model from disk")

loaded_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=['accuracy'])




def evaluation(msg):
    X = [[]]
    splited_msg = msg.split(' ')
    for word in splited_msg:
        if word in search_model_word_table.keys():
            X[0].append(int(search_model_word_table[word]))
    X = sequence.pad_sequences(X, maxlen=20)

    pred = loaded_model.predict(X)

    intent = np.argmax(pred[0])

    if intent == 0:
        return "상품 소개"
    elif intent == 1:
        return "지점 안내"
    elif intent == 2:
        return "상품 추천"

