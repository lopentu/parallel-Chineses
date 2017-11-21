#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
from sklearn.metrics import f1_score, accuracy_score
from keras.models import Model
from keras.layers import Input, Dense, GRU
from keras.preprocessing.text import one_hot, Tokenizer
from keras.preprocessing.sequence import pad_sequences


def get_data(filename):
    data = []

    with open(filename) as f:
        for line in f:
            sp_line = line.strip().split(',')
            text = sp_line[0]
            label = sp_line[1]
            data.append((text, label))

    return data


def train(X, Y):
    c = np.c_[X.reshape(len(X), -1), Y.reshape(len(Y), -1)]
    np.random.shuffle(c)
    X_shuf = c[:, :X.size//len(X)].reshape(X.shape)
    Y_shuf = c[:, X.size//len(X):].reshape(Y.shape)
    print('X_shuf.shape =', X_shuf.shape)
    print('Y_shuf.shape =', Y_shuf.shape)

    inputs = Input(shape=(X.shape[1], X.shape[2]))
    recl = GRU(32)(inputs)
    desl = Dense(Y.shape[1], activation='softmax')(recl)
    model = Model(input=inputs, output=desl)
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    X_train, X_test = X_shuf[200:], X_shuf[:200]
    Y_train, Y_test = Y_shuf[200:], Y_shuf[:200]
    model.fit(X_train, Y_train, batch_size=16, epochs=15)

    pred = model.predict(X_test, verbose=0)
    pred_label = np.argmax(pred, axis=1)
    test_label = np.argmax(Y_test, axis=1)
    top_label = np.empty(200)

    fill_value = 1
    top_label.fill(fill_value)
    print('[assign-top] assign_value = {}'.format(fill_value))
    print('  accuracy          =', accuracy_score(test_label, top_label))
    print('  f1_score(every)   =', f1_score(test_label, top_label, average=None))
    print('  f1_score(micro)   =', f1_score(test_label, top_label, average='micro'))

    fill_value = 2
    top_label.fill(fill_value)
    print('[assign-top] assign_value = {}'.format(fill_value))
    print('  accuracy          =', accuracy_score(test_label, top_label))
    print('  f1_score(every)   =', f1_score(test_label, top_label, average=None))
    print('  f1_score(micro)   =', f1_score(test_label, top_label, average='micro'))

    fill_value = 3
    top_label.fill(fill_value)
    print('[assign-top] assign_value = {}'.format(fill_value))
    print('  accuracy          =', accuracy_score(test_label, top_label))
    print('  f1_score(every)   =', f1_score(test_label, top_label, average=None))
    print('  f1_score(micro)   =', f1_score(test_label, top_label, average='micro'))

    print('[prediction]')
    print('  accuracy          =', accuracy_score(test_label, pred_label))
    print('  f1_score(every)   =', f1_score(test_label, pred_label, average=None))
    print('  f1_score(micro)   =', f1_score(test_label, pred_label, average='micro'))

    return model


if __name__ == '__main__':
    data = get_data('./zuo.csv')
    texts, labels = [list(t) for t in zip(*data)]
    print(texts[:3])
    print(labels[:3])

    # tokenize
    tokenizer = Tokenizer(char_level=True)
    tokenizer.fit_on_texts(texts)
    texts = tokenizer.texts_to_sequences(texts)

    # padding
    texts = pad_sequences(texts, padding='pre')
    print('padded_len =', texts.shape[1])

    seqs = []
    for text in texts:
        seq = np.zeros((24, 912))
        seq[np.arange(24), text] = 1
        seqs.append(seq)
    X_raw = np.array(seqs)
    print('X_raw.shape =', X_raw.shape)

    # one-hot, max_label = 11
    nb_label = 12
    labels = np.array(list(map(int, labels)))
    Y_raw = np.zeros((len(labels), nb_label))
    Y_raw[np.arange(len(labels)), labels] = 1
    print('Y_raw.shape =', Y_raw.shape)

    # training
    train(X_raw, Y_raw)

