import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
from konlpy.tag import Kkma
import random

def save_data_csv():
    word_table = {}
    save_X_data = []
    save_Y_data = []
    with open('./kkk.train', 'r', encoding='utf-8') as pf:
        vec = 1
        for line in pf.read().split('\n'):
            splited_line = line.split(',')

            if splited_line[1] == '예금':
                save_Y_data.append(0)
            elif splited_line[1] == '적금':
                save_Y_data.append(1)
            elif splited_line[1] == '대출':
                save_Y_data.append(2)

            save_X_data.append([])
            for word in splited_line[0].split(' '):
                if word not in word_table.keys():
                    word_table[word] = int(vec)
                    vec += 1

                save_X_data[-1].append(int(word_table[word]))


        print(len(save_X_data), len(save_Y_data))

        df = pd.DataFrame(save_X_data)
        df.to_csv('./X.csv', header=False, index=False, sep='\t', encoding='utf-8')
        df = pd.DataFrame(save_Y_data)
        df.to_csv('./Y.csv', header=False, index=False, sep='\t', encoding='utf-8')

        with open('./word_table.txt', 'w') as f:
            json.dump(word_table, f, ensure_ascii=False)


def add_and_save_test_csv():
    word_table = {}
    with open('./word_table.txt', 'r') as js:
        text = js.read()
        word_table = eval(text)
        print(word_table)
    save_X_data = []
    save_Y_data = []

    with open('./kkk.dev', 'r', encoding='utf-8') as pf:
        vec = 0
        for line in pf.read().split('\n'):
            splited_line = line.split(',')

            if splited_line[1] == '예금':
                save_Y_data.append(0)
            elif splited_line[1] == '적금':
                save_Y_data.append(1)
            elif splited_line[1] == '대출':
                save_Y_data.append(2)

            save_X_data.append([])
            for word in splited_line[0].split(' '):
                if word not in word_table.keys():
                    word_table[word] = int(vec)

                save_X_data[-1].append(int(word_table[word]))

        print(len(save_X_data), len(save_Y_data))

        df = pd.DataFrame(save_X_data)
        df.to_csv('./X_test.csv', header=False, index=False, sep='\t', encoding='utf-8')
        df = pd.DataFrame(save_Y_data)
        df.to_csv('./Y_test.csv', header=False, index=False, sep='\t', encoding='utf-8')


def get_train_data(data_path):
    word_table = {}
    kkma = Kkma()
    max_key = 0
    vectorized_x_data = []
    vectorized_y_data = []

    if os.path.exists('word_table.txt'):
        with open('word_table.txt', 'r') as fd:
            word_table = eval(fd.read())
            max_key = word_table[max(word_table, key=word_table.get)] + 1

    with open(data_path, 'r', encoding='utf-8') as data:
        for line in data.read().split('\n'):
            splited_line = line.split(',')

            if splited_line[-1].strip() == '예금':
                vectorized_y_data.append(0)
            elif splited_line[-1].strip() == '적금':
                vectorized_y_data.append(1)
            elif splited_line[-1].strip() == '대출':
                vectorized_y_data.append(2)

            if len(splited_line) > 2:
                splited_line = [''.join(splited_line[0:-1]), splited_line[-1]]

            vectorized_x_data.append([])
            for voca in kkma.pos(splited_line[0]):
                if voca[0] not in word_table.keys():
                    word_table[voca[0]] = max_key
                    max_key += 1
                vectorized_x_data[-1].append(word_table[voca[0]])

    with open('./word_table.txt', 'w') as f:
        json.dump(word_table, f, ensure_ascii=False)

    return suffle_train_data(vectorized_x_data, vectorized_y_data)


def suffle_train_data(x_data, y_data):
    number_of_class = max(y_data)
    number_list_of_data = []
    train_x = []
    valid_x = []
    train_y = []
    valid_y = []
    temp = []
    for i in range(number_of_class + 1):
        number_list_of_data.append(y_data.count(i))

    for i in range(len(x_data)):
        temp.append([x_data[i], y_data[i]])

    start_index = 0
    for idx, number in enumerate(number_list_of_data):
        train_x += [line for line in temp[start_index: start_index + int(number/2)]]
        valid_x += [line for line in temp[start_index + int(number/2): start_index + number]]
        start_index += number

    random.shuffle(train_x)
    random.shuffle(valid_x)

    for i in range(len(train_x)):
        train_y.append(train_x[i][1])
        train_x[i] = train_x[i][0]
    for i in range(len(valid_x)):
        valid_y.append(valid_x[i][1])
        valid_x[i] = valid_x[i][0]

    return train_x, train_y, valid_x, valid_y


