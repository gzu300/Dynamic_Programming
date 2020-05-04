import numpy as np
import json
from .utils import init_empty_mx, init_global_alignment_mx, init_traceback_mx
'''
'simple' realisation of global alignment by DP. fixed substitution score and GAP panelty.
implemented both forward and traceback algorithms.
traceback can trace multiple optimal paths.
'''

read='GAGGCGA'
template='GAGTGA'


def score(mx, row, column, i, j):
    '''
    forward and record for traceback
    '''
    with open('Dynamic_Programming/input/substitution_mx.json', 'r') as f:
        score = json.load(f)
    match_or_mismatch = score[row[i-1]][column[j-1]]
    GAP = score['GAP']
    direction_list = ['d', 'v', 'h']#'d': diagnal, 'v': vertiacl, 'h': horizontal
    scores = [mx[i-1, j-1] + match_or_mismatch, mx[i-1, j] + GAP, mx[i, j-1] + GAP]
    direction_index = np.argwhere(scores == np.max(scores)).flatten()
    direction = ''.join(direction_list[each] for each in direction_index)
    return max(scores), direction

def global_align(read, template):
    forward_mx = init_global_alignment_mx(read, template)
    traceback_mx = init_traceback_mx(read, template)
    for i, R in enumerate(read, 1):
        for j, T in enumerate(template, 1):
             forward_mx[i, j], traceback_mx[i, j] = score(forward_mx, read, template, i, j)
    return forward_mx, traceback_mx
    
def print_alignment(traceback_mx, read, template):
    '''
    for global alignment, the length of the path equals the length of the longer sequence aligned.
    traceback always starts at the bottom right corner, ends at top left corner. 
    There could be multiple optimal paths
    So create a skeleten list of with its length equals to the longer sequence.
    Each element is a list of dictionary. each dictionary has 'coord' and 'dir'(direction pointer, 'd', 'h', or/and 'v'.
    fill the first element with bottom right corner value.

    iterate through the list and fill the next element based on current element.
    '''
    i, j = traceback_mx.shape[0]-1, traceback_mx.shape[1]-1
    seq1 = np.empty(len(read), dtype=str)
    seq2 = np.empty(len(template), dtype=str)
    def fork(value):
        i, j = value['coord']
        temp_list = []
        if 'd' in value['dir']:
            temp_list.append({'coord': (i-1, j-1), 'dir': traceback_mx[i-1, j-1]})
        if 'v' in value['dir']:
            temp_list.append({'coord': (i-1, j), 'dir': traceback_mx[i-1, j]})
        if 'h' in value['dir']:
            temp_list.append({'coord': (i, j-1), 'dir': traceback_mx[i, j-1]})
        return temp_list

    path = seq1.tolist() if len(seq1)>len(seq2) else seq2.tolist()
    path[0] = [{'coord': (i, j), 'dir': traceback_mx[i, j]}]
    for index, value in enumerate(path):
        temp_list = []
        for each in value:
            temp_list += fork(each)
        if index < len(path)-1:
            temp_list = list({v['coord']:v for v in temp_list}.values()) #remove duplicates in the list
            path[index+1] = temp_list
    print(path)
    return path
   

if __name__=='__main__':
    forward, traceback = global_align(read, template)
    print(forward)

