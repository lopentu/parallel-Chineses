#-*- coding: UTF-8 -*-
from math import log, inf

class BinaryNB():
    def __init__(self):
        self.vocabs = set()
        self.classes = {}
        self.logprior = {}
        self.loglikelihood = {}

    def train(self, data):
        # count words
        for class_name, text in data:
            if class_name not in self.classes:
                self.classes[class_name] = { 'vocabs': {}, 'count': 0, 'nb_word': 0 }
            self.classes[class_name]['count'] += 1

            for word in set(text):
                self.vocabs.add(word)
                if word in self.classes[class_name]['vocabs']:
                    self.classes[class_name]['vocabs'][word] += 1
                else:
                    self.classes[class_name]['vocabs'][word] = 1
            self.classes[class_name]['nb_word'] += 1

        # calculate logprior
        for class_name, class_value in self.classes.items():
            self.logprior[class_name] = log(class_value['count'] / len(data))

        # calculate likelihood
        for word in self.vocabs:
            if word not in self.loglikelihood:
                self.loglikelihood[word] = {}

            for class_name in self.classes:
                if word in self.classes[class_name]['vocabs']:
                    self.loglikelihood[word][class_name] = log((self.classes[class_name]['vocabs'][word] + 1) / (self.classes[class_name]['nb_word'] + len(self.vocabs)))
                else:
                    self.loglikelihood[word][class_name] = log( 1 / (self.classes[class_name]['nb_word'] + len(self.vocabs)))

    def predict(self, data):
        results = []

        for text in data:
            total = self.logprior.copy()
            for word in set(text):
                if word in self.vocabs:
                    for class_name in self.classes:
                        total[class_name] += self.loglikelihood[word][class_name]
                else:
                    for class_name in self.classes:
                        total[class_name] += log( 1 / (self.classes[class_name]['nb_word'] + len(self.vocabs)))

            max_prob = -inf
            max_class = None
            for class_name, prob in total.items():
                if prob > max_prob:
                    max_prob = prob
                    max_class = class_name
            results.append(max_class)

        return results


if __name__ == '__main__':
    from sys import argv
    from utils import read_csvdir, sep_train_test, accuracy

    data_arr = read_csvdir(argv[1])

    total = 0
    times = 100
    for _ in range(times):
        train_arr, test_arr = sep_train_test(data_arr)
        test_Y, test_X = zip(*test_arr)

        print('# of training data =', len(train_arr))
        print('# of test data     =', len(test_arr))

        nb = BinaryNB()
        nb.train(train_arr)
        preds = nb.predict(test_X)

        acc = accuracy(test_Y, preds)
        total += acc
        print('=> accuracy =', acc)

    print('\naccuracy for {} times = {}'.format(times, total / times))
