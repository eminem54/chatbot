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

reverse_input_char_index = dict(
    (i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict(
    (i, char) for char, i in target_token_index.items())




model.save('s2s.h5')

# todo:Next: inference mode (sampling).
# Here's the drill:
# 1) encode input and retrieve initial decoder state
# 2) run one step of decoder with this initial state
# and a "start of sequence" token as target.
# Output will be the next target token
# 3) Repeat with the current target token and current states

print()
# Define sampling models
encoder_model = Model(encoder_inputs, encoder_states)
print("encoder_model:", encoder_model)
decoder_state_input_h = Input(shape=(latent_dim,))
print("decoder_state_input_h", decoder_state_input_h)
decoder_state_input_c = Input(shape=(latent_dim,))
print("decoder_state_input_c", decoder_state_input_c)
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
print("decoder_states_inputs:", decoder_states_inputs)
decoder_outputs, state_h, state_c = x(
    decoder_inputs, initial_state=decoder_states_inputs)
print("decoder_outputs:", decoder_outputs)
decoder_states = [state_h, state_c]
print("decoder_states:", decoder_states)
decoder_outputs = decoder_outputs(decoder_outputs)
print("decoder_outputs:", decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states)
print("decoder_model:", decoder_model)
# Reverse-lookup token index to decode sequences back to
# something readable.


def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_token_index['\t']] = 1.
    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '\n' or
           len(decoded_sentence) > max_decoder_seq_length):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]

    return decoded_sentence

for seq_index in range(100):
    # Take one sequence (part of the training set)
    # for trying out decoding.
    input_seq = encoder_input_data[seq_index: seq_index + 1]
    decoded_sentence = decode_sequence(input_seq)
    print('-')
    print('Input sentence:', input_texts[seq_index])
    print('Decoded sentence:', decoded_sentence)