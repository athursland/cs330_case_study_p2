"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""
from parse import import_data
import csv
import math
import random
import heapq
import time

### define global variables
fn = 'data/geolife-cars-upd8.csv'
t_ids = 'data/trajectory-ids.txt'
global data
global ids

def import_ids(fname):
    ids = []
    with open(fname, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ids.append(row[0])

    return ids

def get_traj(data):
    trajectories = {}
    for row in data:
        print(row)
        if row in ids:
            if row not in trajectories: 
                trajectories[row] = [row]
            else:
                trajectories[row].append(row)
    return trajectories

def approach2(T):
    M = 0
    for t in T: 
        if len(t) > M:
            M = len(t)

    for i in range(len(T)): 
        n = len(t)
        diff = M-n
        j = 0
        while j < diff:
            x = (T[i][1][j][1] + T[i][1][j+1][1])/2
            y = (T[i][1][j][2] + T[i][1][j+1][2])/2
            T[i] = T[i][1][:j+1] + (T[i][1][j+1][0],  x, y) + T[i][1][j+1:]
            j += 1 
        i += 1

    # i = unit of time
    T_c = []
    for i in range(M):
        all_x = []
        all_y = []
        for j in range(len(T)):
            all_x.append(T[j][1][i][1])
            all_y.append(T[j][1][i][2])
        T_c.append((sum(all_x)/len(T), sum(all_y)/len(T)))
        print(T_c)

    return T_c

if __name__=="__main__":
    data = import_data(fn)
    print(data[:5])
    ids = import_ids(t_ids)
    print(ids)
    T = get_traj(ids)
    print(T)
    print(approach2(T.items()))