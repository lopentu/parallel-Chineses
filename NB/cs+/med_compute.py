#-*- coding:UTF-8 -*-
import os
import re
import codecs
import jieba
import csv
from datetime import datetime
from datetime import timedelta

#srt_parsing: from srt file to data ready for NB training

def run_jieba(input_file):
    """
    #input: srt file (encoding utf-8)
    #output: a list of begin time, end time and tokenized text(sep by ' ')
    #[[begin_time, end_time, tokennized_text],...]
    """
    #read in srt file
    f = codecs.open(input_file, 'r+', encoding='utf-8')
    srt = f.read()

    output_list = []

    #define regex to find timestamp, text and sentences
    regex_timetext = re.compile(r'\n(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\r\n(.+?)\r\n\r\n', re.DOTALL)
    regex_sents = re.compile(r'<s>(.+?)\n</s>', re.DOTALL)
    time_text = regex_timetext.findall(srt)

    #load user dictionary, 'dict.txt.big' should be in the same path with input_file
    jieba.load_userdict('./SRT/dict.txt.big')

    for i in range(len(time_text)):
        begin = datetime.strptime(time_text[i][0], '%H:%M:%S,%f')
        end = datetime.strptime(time_text[i][1], '%H:%M:%S,%f')
        output_list.append([begin, end, ""])
        text = time_text[i][2]
        text = text.replace('  -', '\n</s><s>').replace('-', '').replace('  ', '\n</s><s>').replace('\r\n', '\n</s><s>')
        text = '<s>' + text + '\n</s>'
        sentences = regex_sents.findall(text)
        for j in range(len(sentences)):
            sentence = sentences[j]
            #removing letter, number and punc
            sentence = re.sub("[A-Za-z0-9\<\>\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：〝〞]+", "", sentence)
            words = jieba.cut(sentence)
            result = " ".join(words)
            if j == len(sentences) - 1:
                output_list[i][2] += result
            else:
                output_list[i][2] += result + ' '
    return output_list

#simplified transfer to traditional
from langconv import *

def simple2tradition(line):
    line = Converter('zh-hant').convert(line)
    return line


def find_aligned(srt1, srt2):
    """
    #find aligned sentences(begin and end with about the same timestamp)
    #input: srt1(cn), srt2(tw): lists of begin_time, end_time, text returned by run_jieba
    #output: a list containing all aligned sentenses
    #[[cn, tw], [cn, tw],...]
    """
    delta =  timedelta(seconds = 1.1) #define the level to regard two timestamp as about the same, (eg,0 completely the same)
    aligned = []
    i = 0 #index of srt1
    j = 0 #index of srt2
    p = 0 #index of aligned
    discard = 1 #whether to discard a line
    while i < len(srt1):
        #look for the same timestamp in next 5 lines of srt2, if not found, discard this line of srt1
        for k in range(5):
            if (j + k) < len(srt2) and abs(srt1[i][0] - srt2[j + k][0]) < delta: #check begin time is the same
                discard = 0
                aligned.append([simple2tradition(srt1[i][2]), srt2[j + k][2]])
                p += 1
                j += k
                if abs(srt1[i][1] - srt2[j][1]) >= delta: #check end time is the same
                    end = 0;
                    for n in range (5):
                        for m in range(5):
                            if (i + n) < len(srt1) and (j + m) < len(srt2) and abs(srt1[i + n][1] - srt2[j + m][1]) < delta:
                                inew = i + n
                                jnew = j + m
                                end = 1;
                                break;
                        if end == 1:
                            break;
                    while i < inew:
                        i += 1
                        aligned[p - 1][0] += ' ' + simple2tradition(srt1[i][2])
                    while j < jnew:
                        j += 1
                        aligned[p - 1][1] += ' ' + srt2[j][2]
                break;
            else:
                discard = 1
                continue;
        if discard == 1:
            i += 1
        else:
            i += 1
            j += 1
    return aligned


def MED(source, target):
    """
    #compute MED of a pair of aligned sentence
    #input: a source sentece and a target sentence, both tokenized
    #output: a number, MED
    """
    source = source.split()
    target = target.split()
    n = len(source)
    m = len(target)
    d = []
    for i in range(n + 1):
        d.append([])
        for j in range(m + 1):
            d[i].append([])
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            a = d[i - 1][j] + 1
            b = d[i][j - 1] + 1
            if source[i - 1] == target[j - 1]:
                c = d[i - 1][j - 1]
            else:
                c = d[i - 1][j - 1] + 2
            d[i][j] = min(a, b, c)
    return d[n][m]



def srt_pair_MEDS(inputfile1, inputfile2):
    """
    #compute MEDS for a CN file and a TW file
    #input: cn srt file, tw srt file (encoding utf-8)
    #output: MEDS
    """
    time_text_cn = run_jieba(inputfile1)
    time_text_tw = run_jieba(inputfile2)
    aligned_sentences = find_aligned(time_text_cn, time_text_tw)
    MEDS = []
    for pair in aligned_sentences:
        m = max(len(pair[0].split()), len(pair[1].split()))
        med = MED(pair[0], pair[1])
        if m == 0:
            #discard this pair if both are empty string
            continue;
        else:
            MEDS.append([round(float(med)/m, 3), med, pair[0], pair[1]])
    return MEDS

def all_srt_MEDS(srt_list):
    """
    #compute MEDS for a series of pairs of CN file and TW file
    #input: srt_list:[[inputfile1, inputfile2],...]
    #output: MEDS of all the files
    """
    all_MEDS = []
    for pair in srt_list:
        all_MEDS += srt_pair_MEDS(pair[0], pair[1])
        print(pair[0] + ' ' + pair[1] + ' MEDS done.')
    return all_MEDS



if __name__ == '__main__':
    srt_list = [['./SRT/BD_CN.srt', './SRT/BD_TW.srt'],
                ['./SRT/IC_CN.srt', './SRT/IC_TW.srt'],
                ['./SRT/IF_CN.srt', './SRT/IF_TW.srt'],
                ['./SRT/SP_CN.srt', './SRT/SP_TW.srt'],
                ['./SRT/WO_CN.srt', './SRT/WO_TW.srt']]

    all_MEDS = all_srt_MEDS(srt_list)
    f = open('med.csv', 'w')
    writer = csv.writer(f)
    writer.writerows(all_MEDS)
    f.close()
