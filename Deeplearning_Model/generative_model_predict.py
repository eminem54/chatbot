from keras.models import model_from_json
import os
import numpy as np

max_encoder_seq_length = 5
max_decoder_seq_length = 12
num_encoder_tokens = 255
num_decoder_tokens = 303
# dictionary load
input_token_index = {}
if os.path.exists('./Deeplearning_Model/input_token_index.txt'):
    with open('./Deeplearning_Model/input_token_index.txt', 'r') as fd:
        input_token_index = eval(fd.read())

target_token_index = {}
if os.path.exists('./Deeplearning_Model/target_token_index.txt'):
    with open('./Deeplearning_Model/target_token_index.txt', 'r') as fd:
        target_token_index = eval(fd.read())

reverse_input_char_index = {}
if os.path.exists('./Deeplearning_Model/reverse_input_char_index.txt'):
    with open('./Deeplearning_Model/reverse_input_char_index.txt', 'r') as fd:
        reverse_input_char_index = eval(fd.read())

reverse_target_char_index = {}
if os.path.exists('./Deeplearning_Model/reverse_target_char_index.txt'):
    with open('./Deeplearning_Model/reverse_target_char_index.txt', 'r') as fd:
        reverse_target_char_index = eval(fd.read())


#model load
json_file = open("./Deeplearning_Model/encoder_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
encoder_model = model_from_json(loaded_model_json)

encoder_model.load_weights("./Deeplearning_Model/encoder_model.h5")
print("Loaded encoder_model from disk")

json_file = open("./Deeplearning_Model/decoder_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
decoder_model = model_from_json(loaded_model_json)

decoder_model.load_weights("./Deeplearning_Model/decoder_model.h5")
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
    return encoder_input_data


def make_generative_answer(msg):
    input_seq = convert_to_vector(msg)
    decoded_sentence = decode_sequence(input_seq)
    return decoded_sentence


def test_gm():
    question = input('메시지입력 : ')
    print(make_generative_answer(question))