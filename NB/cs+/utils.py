#-*- coding: UTF-8 -*-
import pandas as pd
from os import listdir
from os.path import join, isfile


def read_csvdir(dirname):
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


if __name__ == '__main__':
    from sys import argv
    for tag, text in read_csvdir(argv[1]):
        print(tag + '\t' + text)

