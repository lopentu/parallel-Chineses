#-*- coding: UTF-8 -*-
from math import log, inf


class SimpleNB():
    def __init__(self):
        self.classes = {}
        self.nb_class = 0
        self.vocabs = {}
        self.nb_vocab = 0

    def train(self, data):
        for tag, text in data:
            # count tags
            if tag not in self.classes:
                self.classes[tag] = {'count': 0, 'words': {}, 'nb_word': 0}
                self.nb_class += 1
            self.classes[tag]['count'] += 1

            # count words
            for word in text:
                if word not in self.vocabs:
                    self.vocabs[word] = 1
                if word not in self.classes[tag]['words']:
                    self.classes[tag]['words'][word] = {'count': 0}
                self.classes[tag]['words'][word]['count'] += 1
                self.classes[tag]['nb_word'] += 1

        # count |V|
        self.nb_vocab = len(self.vocabs)

        for tag, tag_obj in self.classes.items():
            # calc P(c)
            tag_obj['prob'] = tag_obj['count'] / len(data)

            # calc P(w|c), with add-one smoothing
            for word, word_obj in tag_obj['words'].items():
                word_obj['prob'] = (word_obj['count'] + 1) / (tag_obj['nb_word'] + self.nb_vocab)

    def predict(self, data):
        predictions = []

        for text in data:
            max_logprob = -inf
            max_flag = ''

            for tag, tag_obj in self.classes.items():
                logprob = log(tag_obj['prob'])

                for word in text:
                    if word not in tag_obj['words']:
                        logprob += log(1 / (tag_obj['nb_word'] + self.nb_vocab))
                    else:
                        logprob += log(tag_obj['words'][word]['prob'])

                if logprob > max_logprob:
                    max_logprob = logprob
                    max_flag = tag

            predictions.append(max_flag)

        return predictions


if __name__ == '__main__':
    from sys import argv
    from utils import read_csvdir, sep_train_test, accuracy

    data_arr = read_csvdir(argv[1])
    train_arr, test_arr = sep_train_test(data_arr)
    test_Y, test_X = zip(*test_arr)

    print('# of training data =', len(train_arr))
    print('# of test data     =', len(test_arr))

    nb = SimpleNB()
    nb.train(train_arr)
    preds = nb.predict(test_X)

    print('=> accuracy =', accuracy(test_Y, preds))
