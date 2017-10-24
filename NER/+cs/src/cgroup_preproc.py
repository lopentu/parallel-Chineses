import re
import os
from itertools import groupby

def extract_cgroup(cg_path):
    if not os.path.exists(cg_path):
        raise FileNotFoundError("%s not found" % cg_path)

    en_pat = re.compile("original = '(?P<en>.*?)'")
    cn_pat = re.compile("zh-(?:cn|hans):(?P<cn>.*?);")
    tw_pat = re.compile("zh-(?:tw|hant):(?P<tw>.*?);")
    fin = open(cg_path, "r", encoding="UTF-8")
    cg_dict = {}
    for ln in fin.readlines():
        if ln.find("type = 'item'") < 0: continue
        try:
            en = en_pat.search(ln).group("en")
            cn = cn_pat.search(ln).group("cn")
            tw = tw_pat.search(ln).group("tw")
            cg_dict[en] = (tw, cn)    
        except AttributeError:
            continue
    
    fin.close()
    return cg_dict

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

