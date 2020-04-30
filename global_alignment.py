import numpy as np
import itertools
'''
'simple' realisation of global alignment by DP. fixed substitution score and GAP panelty.
implemented both forward and traceback algorithms.
traceback can trace multiple optimal paths.
'''

read='GAGGCGA'
template='GAGTGA'
MATCH = 1
MISMATCH = -1
GAP = -2

def init_empty_mx(row, column, d_type=int):
    row_length = len(row)+1
    col_length = len(column)+1 
    mx = np.zeros((row_length, col_length), dtype=d_type) #with padding for first rows and columns
    return mx

def init_traceback_mx(row, column):
    mx = init_empty_mx(row, column, d_type='U5')
    mx[0, 1:]='1'
    mx[1:, 0]='2'
    mx[0, 0] = '0'
    return mx    

def init_mx(row, column):
    mx = init_empty_mx(row, column)
    mx[:, 0] = init_value(GAP, mx.shape[0])
    mx[0, :] = init_value(GAP, mx.shape[1])
    return mx
    
def init_value(gap, length):
    r = np.arange(0, length)
    return gap*r

def score(mx, row, column, i, j):
    '''
    forward and record for traceback
    '''
    match_or_mismatch = MATCH if row[i-1]==column[j-1] else MISMATCH
    direction_list = ['d', 'v', 'h']#'d': diagnal, 'v': vertiacl, 'h': horizontal
    scores = [mx[i-1, j-1] + match_or_mismatch, mx[i-1, j] + GAP, mx[i, j-1] + GAP]
    direction_index = np.argwhere(scores == np.max(scores)).flatten()
    direction = ''.join(direction_list[each] for each in direction_index)
    return max(scores), direction

def global_align(read, template):
    forward_mx = init_mx(read, template)
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
    print_alignment(traceback, read, template)
    print(traceback)

