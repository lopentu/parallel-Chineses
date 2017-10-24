import re
from itertools import groupby

def get_unigram_freq(text_list):
    bg_dict = {}
    cpat = re.compile("[\u3400-\u9fff\uf900-\ufaff]")
    text = "".join(text_list)
    textvec = sorted(cpat.findall(text))
    ch_group = groupby(textvec)
    ch_dict = {ch: len(list(ch_iter)) for 
               ch, ch_iter in ch_group}
    return ch_dict

def get_bigram_freq(text_list):
    bg_dict = {}
    cpat = re.compile("[^\u3400-\u9fff\uf900-\ufaff]")
    for txt in text_list:    
        if len(txt) < 2: continue
        bg_list = [x+y for x, y in zip(txt, txt[1:])] 
        bg_group = groupby(sorted(bg_list))
        for bg, bg_iter in bg_group:
            if cpat.search(bg): continue
            bg_dict[bg] = bg_dict.get(bg, 0) + len(list(bg_iter))
    return bg_dict


def print_dict_by_freq(dict_freq):
    fn = list(dict_freq.keys())
    fn = sorted(fn, key=dict_freq.get, reverse=True)
    print([(x, dict_freq[x]) for x in fn[0:10]])

