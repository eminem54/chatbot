# it is training keras model by word(split whitespace)
# it works successfully on training data


from __future__ import print_function
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding
import numpy as np
from konlpy.tag import Mecab

mecab = Mecab(dicpath="C:\\mecab\\mecab-ko-dic")
batch_size = 10  # Batch size for training.
epochs = 200  # Number of epochs to train for.
latent_dim = 256  # Latent dimensionality of the encoding space.
num_samples = 10000  # Number of samples to train on.
# Path to the data txt file on disk.
data_path = 'mydata.txt'

# Vectorize the data.
input_texts = []
target_texts = []
input_characters = set(" ")
target_characters = set(" ")
with open(data_path, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
for line in lines[: min(num_samples, len(lines) - 1)]:
    input_text, target_text = line.split('\t')
    input_text = "".join([i[0] + " " for i in mecab.pos(input_text)])
    target_text = '\t ' + target_text + ' \n'
    input_texts.append(input_text)
    target_texts.append(target_text)
    for char in input_text.split(' '):
        if char not in input_characters:
            input_characters.add(char)
    for char in target_text.split(' '):
        if char not in target_characters:
            target_characters.add(char)

input_texts.append(" ")
target_texts.append("잘 모르겠네요.")
input_texts.append("  ")
target_texts.append("잘 모르겠네요.")
input_texts.append("   ")
target_texts.append("잘 모르겠네요.")
input_texts.append("    ")
target_texts.append("잘 모르겠네요.")
input_texts.append("     ")
target_texts.append("잘 모르겠네요.")
input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))
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
    [(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict(
    [(char, i) for i, char in enumerate(target_characters)])

print(input_token_index)
print(target_token_index)

encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens),
    dtype='float32')
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype='float32')
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype='float32')

print("인코더 인풋의 shape:", encoder_input_data.shape)
print("디코더 인풋의 shape:", decoder_input_data.shape)
print("디코더 타겟의 shape:", decoder_target_data.shape)


for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text.split(' ')):
        encoder_input_data[i, t, input_token_index[char]] = 1.
    for t, char in enumerate(target_text.split(' ')):
        # decoder_target_data is ahead of decoder_input_data by one timestep
        decoder_input_data[i, t, target_token_index[char]] = 1.
        if t > 0:
            # decoder_target_data will be ahead by one timestep
            # and will not include the start character.
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.



# Define an input sequence and process it.
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
# We discard `encoder_outputs` and only keep the states.
encoder_states = [state_h, state_c]

# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = Input(shape=(None, num_decoder_tokens))
# We set up our decoder to return full output sequences,
# and to return internal states as well. We don't use the
# return states in the training model, but we will use them in inference.
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                     initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model that will turn
# `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Run training
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.2)
# Save model
#model.save('s2s.h5')

# todo:Next: inference mode (sampling).
# Here's the drill:
# 1) encode input and retrieve initial decoder state
# 2) run one step of decoder with this initial state
# and a "start of sequence" token as target.
# Output will be the next target token
# 3) Repeat with the current target token and current states

# Define sampling models
encoder_model = Model(encoder_inputs, encoder_states)

decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(
    decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states)

# Reverse-lookup token index to decode sequences back to
# something readable.
reverse_input_char_index = dict(
    (i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict(
    (i, char) for char, i in target_token_index.items())


# dictionary and model save
import json
import os

with open('./input_token_index.txt', 'w') as f:
    json.dump(input_token_index, f, ensure_ascii=False)
with open('./target_token_index.txt', 'w') as f:
    json.dump(target_token_index, f, ensure_ascii=False)
with open('./reverse_input_char_index.txt', 'w') as f:
    json.dump(reverse_input_char_index, f, ensure_ascii=False)
with open('./reverse_target_char_index.txt', 'w') as f:
    json.dump(reverse_target_char_index, f, ensure_ascii=False)

from keras.models import model_from_json

model_json = encoder_model.to_json()
with open("encoder_model.json", "w") as json_file :
    json_file.write(model_json)
encoder_model.save_weights("encoder_model.h5")

model_json = decoder_model.to_json()
with open("decoder_model.json", "w") as json_file :
    json_file.write(model_json)
decoder_model.save_weights("decoder_model.h5")


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
        print(sampled_token_index)
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




"""
from keras.models import model_from_json
import os
import numpy as np
from konlpy.tag import Mecab

mecab = Mecab(dicpath="C:\\mecab\\mecab-ko-dic")
max_encoder_seq_length = 10
max_decoder_seq_length = 12
num_encoder_tokens = 241
num_decoder_tokens = 352
# dictionary load
input_token_index = {}
if os.path.exists('./input_token_index.txt'):
    with open('./input_token_index.txt', 'r') as fd:
        input_token_index = eval(fd.read())

target_token_index = {}
if os.path.exists('./target_token_index.txt'):
    with open('./target_token_index.txt', 'r') as fd:
        target_token_index = eval(fd.read())

reverse_input_char_index = {}
if os.path.exists('./reverse_input_char_index.txt'):
    with open('./reverse_input_char_index.txt', 'r') as fd:
        reverse_input_char_index = eval(fd.read())

reverse_target_char_index = {}
if os.path.exists('./reverse_target_char_index.txt'):
    with open('./reverse_target_char_index.txt', 'r') as fd:
        reverse_target_char_index = eval(fd.read())


#model load
json_file = open("./encoder_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
encoder_model = model_from_json(loaded_model_json)

encoder_model.load_weights("./encoder_model.h5")
print("Loaded encoder_model from disk")

json_file = open("./decoder_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
decoder_model = model_from_json(loaded_model_json)

decoder_model.load_weights("./decoder_model.h5")
print("Loaded decoder_model from disk")


def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq, steps=2)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_token_index['\t']] = 1.
    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[str(sampled_token_index)]
        decoded_sentence += sampled_char + " "

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '\n' or
           len(decoded_sentence.split(' ')) > max_decoder_seq_length):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]
    return decoded_sentence


def convert_to_vector(text):
    encoder_input_data = np.zeros((1, max_encoder_seq_length, num_encoder_tokens), dtype='float32')
    for t, voca in enumerate(text.split(' ')):
        if voca in input_token_index.keys():
            encoder_input_data[0, t, input_token_index[voca]] = 1.
        else:
            encoder_input_data[0, t, input_token_index[" "]] = 1.
    return encoder_input_data


def make_generative_answer(msg):
    input_seq = convert_to_vector(msg)
    decoded_sentence = decode_sequence(input_seq)
    return decoded_sentence


def test_gm():
    question = input('메시지입력 : ')
    while question != "":
        print(make_generative_answer("".join([i[0] + " " for i in mecab.pos(question)])))
        question = input('메시지입력 : ')

test_gm()
"""