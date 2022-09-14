import os
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

def advanced_flatten_list(alist):
    flattened_list = []
    for element in alist:
        if isinstance(element, list):
            flattened_list.extend(advanced_flatten_list(element))
        else:
            flattened_list.append(element)
    return flattened_list

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

def advanced_split(text, delimiters, maxsplit=0, flags=0, strip=True, keep_delimiter=False, remove_empy=True, join_char=None):
    if keep_delimiter:
        regex_pattern = '|'.join('(?<={})'.format(re.escape(delim)) for delim in delimiters)
    else:
        regex_pattern = '|'.join(map(re.escape, delimiters))

    new = re.split(pattern=regex_pattern,
                   string=text, 
                   maxsplit=maxsplit,
                   flags=flags)

    if strip: new = [element.strip() for element in new]
    if remove_empy: new = [a for a in new if a!='']

    if join_char != None:
        assert keep_delimiter==False, 'Will return the original text'
        new = join_char.join(new)
    
    return new

def advanced_path_join(alist):
    return os.path.join(*advanced_flatten_list(alist))