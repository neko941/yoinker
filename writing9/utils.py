import re

def isfloat(num):
    if int(num) - num == 0:
        return False
    else:
        return True

def flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def isfloatfromstring(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def advanced_split(text, delimiters, maxsplit=0, flags=0, strip=True, keep_delimiter=False):
    if keep_delimiter:
        regex_pattern = '|'.join('(?<={})'.format(re.escape(delim)) for delim in delimiters)
    else:
        regex_pattern = '|'.join(map(re.escape, delimiters))

    new = re.split(pattern=regex_pattern,
                   string=text, 
                   maxsplit=maxsplit,
                   flags=flags)

    if strip: new = [element.strip() for element in new]
    
    return new