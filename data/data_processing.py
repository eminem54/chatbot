import tensorflow as tf
import numpy as np
import pandas as pd
import json

def save_data_csv():
    word_table = {}
    save_X_data = []
    save_Y_data = []
    with open('./data/kkk.train', 'r', encoding='utf-8') as pf:
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
        df.to_csv('./data/X.csv', header=False, index=False, sep='\t', encoding='utf-8')
        df = pd.DataFrame(save_Y_data)
        df.to_csv('./data/Y.csv', header=False, index=False, sep='\t', encoding='utf-8')

        with open('./data/word_table.txt', 'w') as f:
            json.dump(word_table, f, ensure_ascii=False)


def save_test_csv():
    word_table = {}
    with open('./data/word_table.txt', 'r') as js:
        text = js.read()
        word_table = eval(text)
        print(word_table)
    save_X_data = []
    save_Y_data = []

    with open('./data/kkk.dev', 'r', encoding='utf-8') as pf:
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
        df.to_csv('./data/X_test.csv', header=False, index=False, sep='\t', encoding='utf-8')
        df = pd.DataFrame(save_Y_data)
        df.to_csv('./data/Y_test.csv', header=False, index=False, sep='\t', encoding='utf-8')


def get_data1():
    x_data = []
    y_data = []
    x_test = []
    y_test = []
    with open('./data/X.csv', 'r') as pf:
        index = 0
        for line in pf.read().split('\n'):
            if index < 50:
                x_data.append([int(x.rstrip().replace('.0', '')) for x in line.split('\t') if len(x) > 0])
            else:
                x_test.append([int(x.rstrip().replace('.0', '')) for x in line.split('\t') if len(x) > 0])
            index += 1
            if index > 99:
                index = 0

    with open('./data/Y.csv', 'r') as pf2:
        index = 0
        for line in pf2.read().split('\n'):
            if index < 50:
                y_data.append(int(line))
            else:
                y_test.append(int(line))
            index += 1
            if index > 99:
                index = 0

    return x_data, y_data, x_test, y_test

def get_data2():
    x_data = []
    y_data = []
    x_test = []
    y_test = []
    with open('./data/X_test.csv', 'r') as pf:
        index = 0
        for line in pf.read().split('\n'):
            if index < 50:
                x_data.append([int(x.rstrip().replace('.0', '')) for x in line.split('\t') if len(x) > 0])
            else:
                x_test.append([int(x.rstrip().replace('.0', '')) for x in line.split('\t') if len(x) > 0])
            index += 1
            if index > 99:
                index = 0

    with open('./data/Y_test.csv', 'r') as pf2:
        index = 0
        for line in pf2.read().split('\n'):
            if index < 50:
                y_data.append(int(line))
            else:
                y_test.append(int(line))
            index += 1
            if index > 99:
                index = 0

    return x_data, y_data, x_test, y_test