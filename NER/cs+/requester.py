# -*- coding: UTF-8 -*-
import os
import sys
import requests
import pandas as pd


def read_csvdir(dirname, details=False):
    """
    # Arguments
        dirname: the path of directory which contains all *.csv files
        verbose: show read filenames or not

    # Returns:
        a list of tuples like, (tag, text)
    """
    df = pd.DataFrame(columns=['tag', 'text'])

    fnames = [x for x in os.listdir(dirname) if x.endswith('.csv')]
    for fname in fnames:
        pname = os.path.join(dirname, fname)
        csv_df = pd.read_csv(pname)
        if not set(['tag', 'text']).issubset(csv_df.columns):
            print('File: {} doesn\'t have the required column.'.format(pname),
                  file=sys.stderr)
            continue
        df = pd.concat([df, csv_df[['tag', 'text']]], ignore_index=True)

        if details:
            print('Read {} lines from {}'.format(len(csv_df), fname),
                  file=sys.stderr)

    return [tuple(x) for x in df.values]


def request_hanlp_server(server_loc, data):
    for idx, (tag, text) in enumerate(data, 1):
        res = requests.get(server_loc, params={'lang': 'cht', 'text': text})
        if len(res.text) > 0:
            for name in res.text.split(','):
                print('{},{}'.format(tag, name))

        if idx % 10 == 0:
            sys.stderr.write('\rProgress: %.2f%%' % (idx * 100 / len(data)))
            sys.stderr.flush()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csvdir', help='directory of CSVs')
    parser.add_argument('-a', '--address',
                        default='10.5.6.23',
                        help='server address')
    parser.add_argument('-p', '--port',
                        default='1234',
                        help='server port')
    args = parser.parse_args()

    data_arr = read_csvdir(args.csvdir, details=True)
    server_loc = 'http://{}:{}/translated_name'.format(args.address, args.port)

    print('tag,name')
    print(file=sys.stderr)
    request_hanlp_server(server_loc, data_arr)
