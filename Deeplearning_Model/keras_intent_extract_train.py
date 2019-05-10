import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from Deeplearning_Model import data_processing
from keras import optimizers

np.random.seed(7)
X_train, y_train, X_test, y_test = data_processing.get_train_data('../data/kkk.train')

max_review_length = 20
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)
print(X_train[0])

embedding_vector_length = 32

model = Sequential()
model.add(Embedding(400, embedding_vector_length, input_length=max_review_length))
model.add(LSTM(64, input_dim=64, return_sequences=True))
model.add(LSTM(32, return_sequences=True))
model.add(LSTM(16, return_sequences=False))
model.add(Dense(3, activation='sigmoid'))

adam = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(loss='sparse_categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
print(model.summary())

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=10)

scores = model.evaluate(X_test, y_test, verbose=1)

print("Accuracy: %.2f%%" % (scores[1]*100))

model_json = model.to_json()
with open("model.json", "w") as json_file :
    json_file.write(model_json)

model.save_weights("model.h5")
print("Saved model to disk")

