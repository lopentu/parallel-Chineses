import re

def preproc_twname_data(fpath, enc='cp950'):
    fin = open(fpath, "r", encoding=enc, errors='ignore')
    nameRow_pat = re.compile("^\s?\d+")
    tw_names = []
    for ln in fin.readlines():
        if nameRow_pat.search(ln):
            records = re.findall("\d{8}\u3000(...)", ln)
            tw_names += [x.replace("\u3000", "") for x in records]

    # aboriginals has distince name structure
    tw_names = [x for x in tw_names if x.find("‧")<0]       
    return tw_names

def preproc_cnname_data(fpath, enc="utf-8"):
    fin = open(fpath, "r", encoding=enc, errors='ignore')
    nameRow_pat = re.compile("^\s?\d+")
    name_list = []
    for ln in fin.readlines():
        if nameRow_pat.search(ln):            
            toks = [x for x in re.split(" ", ln) if x]        
            if len(toks) < 2: continue
            name_list.append(toks[1])
    return name_list

def print_dict_by_freq(dict_freq):
    fn = list(dict_freq.keys())
    fn = sorted(fn, key=dict_freq.get, reverse=True)
    print([(x, dict_freq[x]) for x in fn[0:10]])