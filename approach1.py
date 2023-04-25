"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""
import math
import import_data
from matplotlib import pyplot as plt

fn = 'data/geolife-cars-upd8.csv'
t_ids = 'data/trajectory-ids.txt'
global ids
global ids_from_txt

#################
##### APPROACH 1
#################

def approach1(trajectories): 
    """
    input: nested list of trajectories, each list contains int tuples of (x,y) coords
    output: center trajectory as a list of int tuples
    """
    min_dist = float('inf')
    center = None
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
    """
    input: two lists of int tuples seriesA and seriesB
    output: sum of euclidian distances between seriesA and seriesB
    """
    A = seriesA
    B = seriesB
    n = len(seriesA)
    m = len(seriesB)

    ### original attempt
    
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

    return DP[n-1][m-1]

#Distance Formula
def dist(a, b):
  return math.dist([a[0], a[1]], [b[0], b[1]])

#################
##### EXPERIMENTS
#################

def visualize(T, T_c):
    """
    input: T = list of ids of trajectories, T_c = input trajectory as list of int tuples 
    output: visualization of chosen center trajectory vs. all other trajectories in trajectory-ids.txt 
    """
    T_x = []
    T_y = []

    for k in T: # for each trajectory in t_ids
        t = traj_dict.get(k)
        T_x.append([p[0] for p in t])
        T_y.append([p[1] for p in t])
    
    T_c_x = [p[0] for p in T_c]
    T_c_y = [p[1] for p in T_c]

    colors = ['b', 'g', 'y', 'c', 'm', 'purple', 'olive', 'brown', 'pink', 'gray', 'black']
    for i in range(len(T)):
        plt.plot(T_x[i], T_y[i], color = colors[i], linewidth = 0.7, alpha = 0.8, label = 'trajectory {}'.format(i))

    plt.plot(T_c_x, T_c_y, color = 'r', linewidth = 0.8, label = 'approach 2 center')
    plt.title('Given trajectories and computed trajectory center')
    plt.xlabel('x-coordinates')
    plt.ylabel('y-coordinates')
    plt.legend()

    plt.show()

    return 

def get_avg_dist(T, T_c):
    avg_dists = []
    M = len(T_c)
    
    for traj in T: 
        d_sum = 0
        t = ids_from_txt.get(traj)
        n = len(t)
        for i in range(n):
            closest_d = float('inf')
            for j in range(M):
                d = dist(t[i], T_c[j])
                if d < closest_d:
                        closest_d = d
            d_sum += closest_d
        avg_dists.append(d_sum/n)

    L = ["avg dist to trajectory {}: {}\n".format(i, avg_dists[i]) for i in range(len(T))]
    with open('approach1_avg_dists.txt'.format(i), 'w') as file1:
        file1.writelines(L)
    return avg_dists

def visualize(T, T_c):
    T_x = []
    T_y = []

    for k in T: # for each trajectory in t_ids
        t = traj_dict.get(k)
        T_x.append([p[0] for p in t])
        T_y.append([p[1] for p in t])
    
    T_c_x = [p[0] for p in T_c]
    T_c_y = [p[1] for p in T_c]

    colors = ['b', 'g', 'y', 'c', 'm', 'purple', 'olive', 'brown', 'pink', 'gray', 'black']
    for i in range(len(T)):
        plt.plot(T_x[i], T_y[i], color = colors[i], linewidth = 0.7, alpha = 0.8, label = 't_{}'.format(i))

    plt.plot(T_c_x, T_c_y, color = 'r', linewidth = 0.8, label = 'approach 1 T_c')
    plt.title('Input trajectories and T_c')
    plt.xlabel('x-coord')
    plt.ylabel('y-coord')
    plt.legend()

    plt.show()

    return 

if __name__=="__main__":
    data = import_data.import_data(fn)
    ids = import_data.import_ids(t_ids) 
    traj_dict = import_data.get_traj(data) # this contains ALL of the trajectories
    ids_from_txt = {key: traj_dict[key] for key in traj_dict if key in ids}
    T_c = approach1(list(ids_from_txt.values()))

    get_avg_dist(ids_from_txt.keys(), T_c)
    #visualize(ids_from_txt, T_c)
    
    ### simplify results 0.03 0.1 0.3 
    """
    eps = [0.03, 0.1, 0.3]
    for i in range(3):
        ids_from_txt = {key: simplify.simplify_trajectory(traj_dict[key], eps[i]) for key in traj_dict if key in ids} # dictionary list comprehension to filter for just the ones from the txt file
        T_c = approach1(list(ids_from_txt.values()))
        get_avg_dist(ids_from_txt.keys(), T_c, i)
    """
