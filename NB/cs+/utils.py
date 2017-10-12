#-*- coding: UTF-8 -*-
import os
import pandas as pd
from random import shuffle


def read_csvdir(dirname, tokenize=True):
    """
    # Arguments
        dirname: the path of directory which contains all *.csv files
        tokenize: tokenize sentences or not
    
    # Returns:
        a list of tuples like, (tag, text)
    """
    df = pd.DataFrame(columns=['tag', 'text'])

    fnames = [x for x in os.listdir(dirname) if x.endswith('.csv')]
    for fname in fnames:
        pname = os.path.join(dirname, fname)
        csv_df = pd.read_csv(pname)
        if not set(['tag', 'text']).issubset(csv_df.columns):
            print('File: {}, does not contain the required columns.'.format(pname))
            continue
        df = pd.concat([df, csv_df[['tag', 'text']]], ignore_index=True)

    # data are tokenized with 'dict.txt.big' by jieba 
    # cs+/
    # ├── dict.txt.big (must be in the same dir)
    # └── utils.py
    if tokenize:
        currdir_path = os.path.dirname(os.path.realpath(__file__))
        dict_path = os.path.join(currdir_path, 'dict.txt.big')
        if os.path.isfile(dict_path):
            import jieba
            jieba.load_userdict(dict_path)
            df['text'] = df['text'].map(lambda x: list(jieba.cut(x)))

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
