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
from matplotlib import pyplot as plt

### define global variables
fn = 'data/geolife-cars-upd8.csv'
t_ids = 'data/trajectory-ids.txt'
global data
global ids

############################
##### SIMPLIFY TRAJECTORY 
############################

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def dotProduct(A,B):
    return A[0]*B[0]+A[1]*B[1]

def dist_point_segment(q, e): #d in the case study doc
    # Compute the squared length of the segment e
    a = e[0]
    b = e[1]
    l2 = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    #return distance to closest of the endpoints
    if l2 == 0:
        return min(dist(q, a), dist(q,b))

    AB = [e[1][0]-e[0][0],e[1][1]-e[0][1]]
    AQ = [q[0]-e[0][0],q[1]-e[0][1]]
    BQ = [q[0]-e[1][0],q[1]-e[1][1]]
    if dotProduct(AB,AQ)==0 or dotProduct(AB,BQ)==0:
        return (abs(((b[0] - a[0])* (a[1]-q[1])) - ((a[0] - q[0]) * (b[1]-a[1])))/ math.sqrt(l2))
    else:
        return min(dist((e[0][0],e[0][1]),q),dist((e[1][0],e[1][1]),q))

#function that returns the 2 points closest to p from list of points
def closest_points(p, points):
    closest, second_closest = None, None
    min_dist, sec_min_dist = math.inf, math.inf
    for point in points:
        if dist(p, point) < min_dist:
            second_closest = closest
            sec_min_dist = min_dist
            closest = point
            min_dist = dist(p, point)
        elif dist(p, point) < sec_min_dist:
            second_closest = point
            sec_min_dist = dist(p, point)

    return closest, second_closest

def simplify_trajectory(T, eps):
    if len(T) < 3:
       # Base case: return the input trajectory if it has 2 or fewer points
       return []

    T_start=T[0]
    T_end=T[-1]

    max_dist, max_idx = max((dist_point_segment(T[i], (T_start, T_end)), i) for i in range(1, len(T) - 1))
    
    if max_dist>eps:
       simplified_left= simplify_trajectory(T[:max_idx+1],eps)
       simplified_right= simplify_trajectory(T[max_idx:],eps)
       return simplified_left[:-1] + simplified_right
       #simplify_trajectory(T[maxDpoint:],eps)
    else:
       return [T[0],T[-1]]

#################
##### APPROACH 2
#################

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
    """
    input: keys from the dictionary
    """
    M = 0
    for t in T:
        t_n = len(traj_dict.get(t))
        if t_n > M:
            M = t_n
    
    print("MAX # POINTS: ", M)

    for i in range(len(T)):
        for _ in range(2):
            # i = index of trajectory in T
            t = traj_dict.get(T[i])
            n = len(t)
            diff = M-n-1
            j = 0
            while j < (min(diff, n-1))*2: 
                x = (t[j][0] + t[j+1][0])/2
                y = (t[j][1] + t[j+1][1])/2
                t = t[:j+1] + [(x,y)] + t[j+1:]
                j += 2
            if len(t) == M-1: 
                x = (t[-1][0] + t[-2][0])/2
                y = (t[-1][1] + t[-2][1])/2
                t = t[:-1] + [(x,y)] + t[-1:]
            traj_dict[T[i]] = t 
    
    T_c = []
    for i in range(M): # unit of time 
        all_x = []
        all_y = []
        for j in range(len(T)):
            all_x.append(traj_dict.get(T[j])[i][0])
            all_y.append(traj_dict.get(T[j])[i][1])
        T_c.append((sum(all_x)/len(T), sum(all_y)/len(T)))

    return T_c

#################
##### APPROACH 1
#################

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

#########################
##### TASK 3.2: VISUALIZE
#########################

def visualize(T, T_c):
    T_x = []
    T_y = []

    for k in T: # for each trajectory in t_ids
        t = traj_dict.get(k)
        T_x.append([p[0] for p in t])
        T_y.append([p[1] for p in t])
    
    T_c_x = [p[0] for p in T_c]
    T_c_y = [p[1] for p in T_c]

    """
    for i in range(len(T)):
        plt.plot(T_x[i], T_y[i], color = 'blue', linewidth = 0.7, label = 'trajectory')
    """

    plt.plot(T_x[0], T_y[0], color = 'blue', linewidth = 0.7, label = 't1')
    plt.plot(T_x[1], T_y[1], color = 'orange', linewidth = 0.7, label = 't2')
    plt.plot(T_x[2], T_y[2], color = 'green', linewidth = 0.7, label = 't3')
    plt.plot(T_c_x, T_c_y, color = 'red', linewidth = 0.5, label = 'center trajectory')

    plt.title('Approach 1 trajectories vs. trajectory center')
    plt.xlabel('x-coordinates')
    plt.ylabel('y-coordinates')

    plt.show()

    return 


#################
##### MAIN
#################

if __name__=="__main__":
    ### import data
    global traj_dict
    data = import_data(fn) # this is fine 
    ids = import_ids(t_ids) # this is also fine
    
#   ## visualize results of approach 1

    ### visualize results of approach 2
    traj_dict = get_traj(data)
    T_c = approach2(list(traj_dict.keys())) # pass keys, NOT values, then use get
    print(T_c)
    visualize(traj_dict.keys(), T_c)
    