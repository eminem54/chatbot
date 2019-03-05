from keras.models import model_from_json
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy as np
from konlpy.tag import Kkma


def evaluation(msg):
    word_table = {}
    kkma = Kkma()

    with open('word_table.txt', 'r') as js:
        text = js.read()
        word_table = eval(text)

    X = [[]]
    splited_msg = kkma.pos(msg)
    for word in splited_msg:
        if word[0] in word_table.keys():
            X[0].append(int(word_table[word[0]]))

    X = sequence.pad_sequences(X, maxlen=20)

    json_file = open("model.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    loaded_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    # model evaluation

    pred =  loaded_model.predict(X)

    intent = np.argmax(pred[0])
    if intent == 0:
        return "상품 소개"
    elif intent == 1:
        return "지점 안내"
    elif intent == 2:
        return "고객 상담"

#print(evaluation('예금 정보 알려줘'))