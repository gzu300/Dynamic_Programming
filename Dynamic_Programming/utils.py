import numpy as np
import json

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

def init_global_alignment_mx(row, column):
    mx = init_empty_mx(row, column)
    mx[:, 0] = init_margin_value(GAP, mx.shape[0])
    mx[0, :] = init_margin_value(GAP, mx.shape[1])
    return mx
    
def init_margin_value(gap, length):
    r = np.arange(0, length)
    return gap*r

def naive_nt_substitution_mx(match, mismatch, gap):
    nts = ['A', 'T', 'C', 'G']
    base_score = dict(zip(nts, (np.ones(4, dtype=int)*mismatch).tolist()))#json incompatible with numpy dtype
    sub_mx = {}
    for nt in nts:
        a=base_score.copy()
        a[nt] = match
        sub_mx[nt] = a

    sub_mx['GAP'] = gap
    with open('Dynamic_Programming/input/substitution_mx.json', 'w') as f:
        json.dump(sub_mx, f)

if __name__ == '__main__':
    naive_nt_substitution_mx(1, -1, -2)