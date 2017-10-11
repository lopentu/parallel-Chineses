#-*- coding: UTF-8 -*-
import pandas as pd
from os import listdir
from os.path import join, isfile
from random import shuffle


def read_csvdir(dirname):
    """
    # Arguments
        dirname: the path of directory which contains all *.csv files
    
    # Returns:
        a list of tuples like, (tag, text)
    """
    df = pd.DataFrame(columns=['tag', 'text'])

    fnames = [x for x in listdir(dirname) if x.endswith('.csv')]
    for fname in fnames:
        pname = join(dirname, fname)
        csv_df = pd.read_csv(pname)
        if not set(['tag', 'text']).issubset(csv_df.columns):
            print('File: {}, does not contain the required columns.'.format(pname))
            continue
        df = pd.concat([df, csv_df[['tag', 'text']]], ignore_index=True)

    return [tuple(x) for x in df.values]


def sep_train_test(lst, ratio=0.1):
    """
    # Arguments
        lst: any list-like object
        ratio: the ratio of test data to all data
    
    # Returns
        (list_of_training_data, list_of_test_data)
    """
    shuffle(lst)
    thred = int(len(lst) * ratio)
    return lst[thred:], lst[:thred]


if __name__ == '__main__':
    from sys import argv
    data_arr = read_csvdir(argv[1])
    train_arr, test_arr = sep_train_test(data_arr)
    print('# of all read data =', len(data_arr))
    print('# of training data =', len(train_arr))
    for tag, text in train_arr[:5]:
        print('  ', tag, '\t', text)
    print('# of test data     =', len(test_arr))
    for tag, text in test_arr[:5]:
        print('  ', tag, '\t', text)
