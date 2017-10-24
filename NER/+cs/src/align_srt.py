import pdb

def compare_srt_time(item_a, item_b):
    to_sec = lambda x: x[0]*3600 + x[1]*60 + x[2]
    a_start = item_a["start"]
    a_end = item_a["end"]
    b_start = item_b["start"]
    b_end = item_b["end"]
        
    start_diff = abs(to_sec(a_start)-to_sec(b_start))        
    end_diff = abs(to_sec(a_end)-to_sec(b_end))        
    return start_diff + end_diff

def align_srt(srt_a, srt_b):
    cur_b = 0
    align_b = []
    align_idx = -1
    for a_item in srt_a:
        if not a_item["text"]: 
            align_b.append(None)
            continue
        grad = 0
        prev_diff = 1000
        min_diff = 1000
        cur_b_start = max(align_idx-3, 0)
        for cur_b in range(cur_b_start, len(srt_b)):
            b_item = srt_b[cur_b]
            if not b_item["text"]:
                continue
            diff = compare_srt_time(a_item, b_item)
            grad = diff - prev_diff
            if diff < min_diff:
                min_diff = diff
                align_idx = cur_b
            if grad > 0:
                break
        align_b.append(align_idx)    
    return align_b
