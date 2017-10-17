#-*- coding: UTF-8 -*-
from math import log, inf
import numpy as np

class tfidfNB():
    def __init__(self):
        self.vocabs = set()
        self.classes = {1:{'vocabs':{}, 'count':0}, 0:{'vocabs':{}, 'count':0}}
        self.logprior = {}
        self.loglikelyhood = {}

    # Compute tfidf(word, text, data)
    def TFIDF(text, train):

        # Initiailize tfidf for given text
        tfidf_text = np.zeros(len(text))

        # Initiailize number of texts containing a word
        num_text_word = 0

        # Intialize index for words in text
        word_index = 0

        # Go over all words in text
        for word in text:

            # Compute term frequence (tf)
            # Count frequency of word in text
            tf = text.count(word)

            # Find number of texts containing word
            for data in train:

                # Increment word counter if word found in text
                if data[1].count(word) > 0:
                    num_text_word += 1

            # Compute inverse document frequency (idf)
            # log(Total number of texts/number of texts with word)
            idf = np.log(len(train)/num_text_word)

            # Update tf-idf weight for word
            tfidf_text[word_index] = tf*idf

            # Reset text containing word counter
            num_text_word = 0

            # Move onto next word in text
            word_index += 1

        return tfidf_text

    def train(self, data):
        # calculate tfidf
        for class_name, text in data:
            self.classes[class_name]['count'] += 1
            tfidf_text = tfidfNB.TFIDF(text, data)
            tfidf_dict = {}
            for i in range(len(text)):
                if text[i] not in tfidf_dict:
                    tfidf_dict[text[i]] = tfidf_text[i]
            for word in set(text):
                tfidf_word = tfidf_dict[word]
                self.vocabs.add(word)
                if word in self.classes[class_name]['vocabs']:
                    self.classes[class_name]['vocabs'][word] += tfidf_word
                else:
                    self.classes[class_name]['vocabs'][word] = tfidf_word

        # calculate logprior
        for class_name, class_value in self.classes.items():
            self.logprior[class_name] = log(class_value['count'] / len(data))

        # calculate loglikelyhood
        for word in self.vocabs:
            if word not in self.loglikelyhood:
                self.loglikelyhood[word] = {}

            for class_name in self.classes:
                if word in self.classes[class_name]['vocabs']:
                    self.loglikelyhood[word][class_name] = log((self.classes[class_name]['vocabs'][word] + 1)/(sum(self.classes[class_name]['vocabs'].values()) + len(self.vocabs)))
                else:
                    self.loglikelyhood[word][class_name] = log( 1 / (sum(self.classes[class_name]['vocabs'].values()) + len(self.vocabs)))

    def predict(self, data):
        results = []

        for text in data:
            total = self.logprior.copy()
            for word in set(text):
                if word in self.vocabs:
                    for class_name in self.classes:
                        total[class_name] += self.loglikelyhood[word][class_name]
                else:
                    for class_name in self.classes:
                        total[class_name] += log(1 / (sum(self.classes[class_name]['vocabs'].values()) + len(self.vocabs)))

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
