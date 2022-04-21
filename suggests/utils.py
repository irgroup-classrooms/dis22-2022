import re
import os
import json
import random, itertools
import pandas as pd
pd.set_option('max.column', 99)

from timeit import default_timer
from string import ascii_letters, digits

# Files ------------------------------------------------------------------------

def all_abs_paths(dir):
    file_paths = []
    for folder, subs, files in os.walk(dir):
        for filename in files:
            file_paths.append(os.path.abspath(os.path.join(folder, filename)))
    return file_paths

def read_lines(fp):
    with open(fp, 'r') as infile:
        if '.txt' in fp: return [line.strip() for line in infile]
        elif '.json' in fp:  return [json.loads(line.strip()) for line in infile]

def write_lines(iter_data, fp, overwrite=False):
    mode = 'w' if overwrite else 'a+'
    with open(fp, mode) as outfile:
        if '.txt' in fp:
            for data in iter_data:
                outfile.write('%s\n' % data)
        elif '.json' in fp:
            for data in iter_data:
                outfile.write('%s\n' % json.dumps(data))

# Descriptive Stats ------------------------------------------------------------

def dnum(df_col):
    if df_col.dtype in [int, float]:
        return df_col.describe()
    else:
        return 0

def dft(dfcol):
    tab = pd.DataFrame({
        'n': dfcol.value_counts(),
        'p': dfcol.value_counts(True)
    }).sort_index()
    return tab

# Lists ------------------------------------------------------------------------

def unlist(nested_list):
    return list(itertools.chain.from_iterable(nested_list))

# Strings ----------------------------------------------------------------------

def split_by_spaces(s, n=2):
    # Split a string by n or more spaces
    return re.split('\s{%d,}' % n, s)

def get_between_brackets(s, regex=r'\[(.*?)\]'):
    return re.search(regex, s).group(1)

def get_between_parentheses(s, regex=r'\((.*?)\)'):
    return re.search(regex, s).group(1)
    
def remove_digits(string):
    return "".join([x for x in string if not x.isdigit()]).strip()

# Timer ------------------------------------------------------------------------

def start_timer():
    return default_timer()

def stop_timer(start, v=False):
    stop = default_timer()
    total_time = stop - start
    mins, secs = divmod(total_time, 60)
    hours, mins = divmod(mins, 60)
    runtime = f'{int(hours)}:{int(mins)}:{secs}'
    if v:
        print(f'Run time:\t{runtime}\n')
    return f'{runtime}'

# Misc -------------------------------------------------------------------------

def alphanumerics():
    """Generate upper and lowercase letters and digits"""
    return ascii_letters + digits

def random_string(length=12):
    """Generate a random string of alphanumerics"""
    return ''.join(random.choice(alphanumerics()) for i in range(length))

def write_latex_df(df, filename, index=False):
    """Write a latex table from a pd.DataFrame"""
    latex = df.to_latex(index=index)
    with open(filename, 'w') as f:
        f.write(latex)
    print('Saved as: ' + filename)