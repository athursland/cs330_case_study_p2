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
import matplotlib

### define global variables
fn = 'data/geolife-cars-upd8.csv'
t_ids = 'data/trajectory-ids.txt'
global data
global ids

# import trajectory ids
def import_ids(fname):
    ids = []
    with open(fname, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ids.append(row[0])

    return ids

# process trajectory data
def get_traj(data):
    """
    returns a dict where k = t_id and v = datapoints for given trajectory
    """
    trajectories = {}
    for row in data:
        #print(row[0])
        if row[0] in ids:
            if row[0] not in trajectories:
                trajectories[row[0]] = []
            trajectories[row[0]].append((row[1], row[2]))
    return trajectories

def approach2(T):
    M = 0
    for t in T:
        if len(t) > M:
            M = len(t)

    for i in range(len(T)):
        # i = index of trajectory in T
        n = len(T[i]) # number of points in t 
        diff = M-n
        j = 0
        while j < diff:
            x = (T[i][j][0] + T[i][j+1][0])/2
            #x = (T[i][1][j][0] + T[i][1][j+1][0])/2
            y = (T[i][j][1] + T[i][j+1][1])/2
            #y = (T[i][1][j][1] + T[i][1][j+1][1])/2
            T[i] = T[i][:j+1] + [(T[i][j+1][0],  x, y)] + T[i][j+1:]
            j += 1 
        i += 1

    # i = unit of time
    T_c = []
    #print("M: ", M)
    for i in range(M):
        all_x = []
        all_y = []
        for j in range(len(T)):
            all_x.append(T[j][i][0])
            all_y.append(T[j][i][1])
        #print('all_x: ', all_x)
        #print("all_y", all_y)
        T_c.append((sum(all_x)/len(T), sum(all_y)/len(T)))
        print(len(T_c))

    return T_c

def approach_1(trajectories): #want trajectories as a dictionary with id as
   # key and list of tuples as value
   min_dist = float('inf')
   center = None
   #print(trajectories)
   for t_i in trajectories:
       total_distance = 0
       for t_j in trajectories:
           if t_i is not t_j:
               total_distance += dtw(t_i, t_j)
       if total_distance < min_dist:
           min_dist = total_distance
           center = t_i
   return center

def dtw(seriesA, seriesB):
   A = seriesA
   B = seriesB
   n = len(seriesA)
   m = len(seriesB)
   #base cases, fill first and if any series is 1 element
   DP = [[None for _ in range(m)] for _ in range(n)]
   DP[0][0] = dist(A[0], B[0])
   for j in range(1, m):
       DP[0][j] = DP[0][j - 1] + (dist(A[0], B[j]) ** 2)

   for i in range(1, n):
       DP[i][0] = DP[i - 1][0] + (dist(A[i], B[0]) ** 2)

   for i in range(1, n):
       for j in range(1, m):
           DP[i][j] = (dist(A[i], B[j]) ** 2)  + min(DP[i][j - 1], DP[i -
                                                                      1][j],
                                            DP[i - 1][j - 1])

   def find_min(n, m):
       min = (0, m)
       for i in range(1, n):
           if DP[i][m] < DP[min[0]][min[1]]:
               min = (i, m)
       return min #function to find the minimum distance b/w points

   distances = []

   for k in range(0, m):
       pair = find_min(n, k)
       distances.append(dist(A[pair[0]], B[pair[1]]))

   return DP[n - 1][m - 1]


#Distance Formula
def dist(a, b):
  return math.dist([a[0], a[1]], [b[0], b[1]])

if __name__=="__main__":
    data = import_data(fn) # this is fine 
    ids = import_ids(t_ids) # this is also fine
    T = get_traj(data)
    #print(T.get('115-20080527225031'))
    #print(approach2(list(T.values())))
    print(approach_1(list(T.values())))
    