import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
from keras import layers
import sys, os
import random

from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding

batch_size = 64  # Batch size for training.
epochs = 1  # Number of epochs to train for.
latent_dim = 256  # Latent dimensionality of the encoding space.
num_samples = 10000  # Number of samples to train on.
data_path = 'mydata.txt'


input_texts = []
target_texts =[]
input_characters = set()
target_characters = set()
with open(data_path, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
for line in lines[: min(num_samples, len(lines) - 1)]:
    input_text, target_text = line.split('\t')
    target_text = '<SOS> ' + target_text + ' <EOS>'
    input_texts.append(input_text)
    target_texts.append(target_text)
    for voca in input_text.split(' '):
        if voca not in input_characters:
            input_characters.add(voca)
    for voca in target_text.split(' '):
        if voca not in target_characters:
            target_characters.add(voca)

num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt.split(' ')) for txt in input_texts])
max_decoder_seq_length = max([len(txt.split(' ')) for txt in target_texts])

print('데이터 문장 개수:', len(input_texts))
print('고유한 인풋데이터   토큰 개수:', num_encoder_tokens)
print('고유한 아웃풋데이터 토큰 개수:', num_decoder_tokens)
print('가장 긴 인풋데이터   시퀀스 길이:', max_encoder_seq_length)
print('가장 긴 아웃풋데이터 시퀀스 길이:', max_decoder_seq_length)

input_token_index = dict(
    [(voca, i) for i, voca in enumerate(input_characters)])
target_token_index = dict(
    [(voca, i) for i, voca in enumerate(target_characters)])

print(input_token_index)
print(target_token_index)

encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length),
    dtype='float32')
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length),
    dtype='float32')
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype='float32')

print("인코더 인풋의 shape:", encoder_input_data.shape)
print("디코더 인풋의 shape:", decoder_input_data.shape)
print("디코더 타겟의 shape:", decoder_target_data.shape)


for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text.split(' ')):
        encoder_input_data[i, t] = float(input_token_index[char])
    for t, char in enumerate(target_text.split(' ')):
        decoder_input_data[i, t] = float(target_token_index[char])
        if t > 0:
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.

# Define an input sequence and process it.
encoder_inputs = Input(shape=(None,))
print("인코더 인풋 모델:", encoder_inputs)

x = Embedding(max_encoder_seq_length, latent_dim)(encoder_inputs)
print(x,111)
x, state_h, state_c = LSTM(latent_dim, return_state=True)(x)
encoder_states = [state_h, state_c]
print(x,333)
print(encoder_states,444)
# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = Input(shape=(None,))
print("디코더 인풋 모델:", decoder_inputs)
x = Embedding(max_decoder_seq_length, latent_dim)(decoder_inputs)
print(x,666)
x = LSTM(latent_dim, return_sequences=True)(x, initial_state=encoder_states)
print(x,777)
decoder_outputs = Dense(num_decoder_tokens, activation='softmax')(x)
print("디코더 아웃풋 모델:", decoder_outputs)
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile & run training
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.2)