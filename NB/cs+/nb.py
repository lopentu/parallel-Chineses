#-*- coding: UTF-8 -*-
from utils import sep_train_test, accuracy
import numpy as np
import pandas as pd
import sys
import csv

def tag_text(all_MEDS, LIMIT = 0):
    """
    #ouput data for NB training
    #input: all_MEDS
    #output: a list of tag-text
    #[[tag, text],...]
    #tag:1-TW, 0-CN
    #LIMIT: a real number, define the level to discard a pair of sentences as nuetral data,
    #eg: default LIMIT = 0, discard completely the same pairs)
    """

    output_data = []
    for data in all_MEDS:
        if float(data[0]) <= LIMIT:
            #discard this line
            continue;
        else:
            if data[2] != '':
                output_data.append(['CN', data[2].split()])
            if data[3] != '':
                output_data.append(['TW', data[3].split()])
    return output_data


if __name__ == '__main__':

    model = sys.argv[1]
    if (model == 'simple'):
        from simple_nb import SimpleNB as NB
        times = 100
    elif (model == 'binary'):
        from binary_nb import BinaryNB as NB
        times = 100
    elif (model == 'tfidf'):
        from tfidf_nb import tfidfNB as NB
        times = 3

    limits = [0, 0.5, 1, 1.5]

    for limit in limits:

        f = open('med.csv', 'r')
        all_MEDS = csv.reader(f)
        #derive a data set for each limit
        data_arr = tag_text(all_MEDS, LIMIT = limit)

        train_arr, test_arr = sep_train_test(data_arr)
        print('# of training data =', len(train_arr))
        print('# of test data     =', len(test_arr))

        total = 0
        for i in range(times):
            train_arr, test_arr = sep_train_test(data_arr)
            test_Y, test_X = zip(*test_arr)
            nb = NB()
            nb.train(train_arr)
            preds = nb.predict(test_X)
            acc = accuracy(test_Y, preds)
            total += acc

        print('accuracy for model {}, limit {}, times {} = {}\n'.format(model, limit, times, total / times))
