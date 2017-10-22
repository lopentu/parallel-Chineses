import re
import pdb

serial_pat = re.compile("^[\ufeff]?\d+$")
timestamp_pat = re.compile("(?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2}),\d{3}")

def load_srt(fpath):
    fin = open(fpath, "r", encoding="UTF-8")
    buf = []
    srt_list = []
    start = None
    end = None

    for ln in fin.readlines():
        m_serial = serial_pat.search(ln)
        if m_serial:
            srt_list.append({
                "text": "\n".join(buf),
                "start": start,
                "end": end
            })
            # pdb.set_trace()
            buf = []            
            start = None; end = None
            serial = m_serial.group()
            continue

        iter_timestamp = list(timestamp_pat.finditer(ln))
        if iter_timestamp:
            try:
                m_start = iter_timestamp[0]
                start = (int(m_start.group("H")), 
                         int(m_start.group("M")),
                         int(m_start.group("S")))
                m_end = iter_timestamp[1]
                end = (int(m_end.group("H")), 
                       int(m_end.group("M")),
                       int(m_end.group("S")))
            except Exception as ex:
                print(ex)                
            continue

        if ln.strip():
            buf.append(ln.strip())
    
    srt_list = [x for x in srt_list if x["text"]]
    return srt_list
