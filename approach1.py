"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""
import math
import import_data
from matplotlib import pyplot as plt
import simplify

fn = 'data/geolife-cars-upd8.csv'
t_ids = 'data/trajectory-ids.txt'
global ids
global ids_from_txt

#################
##### APPROACH 1
#################

def approach1(trajectories): #want trajectories as a list of trajectories so T.values()
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

#################
##### EXPERIMENTS
#################

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
        plt.plot(T_x[i], T_y[i], color = colors[i], linewidth = 0.7, alpha = 0.8, label = 'trajectory {}'.format(i))

    plt.plot(T_c_x, T_c_y, color = 'r', linewidth = 0.8, label = 'approach 2 center')
    plt.title('Given trajectories and computed trajectory center')
    plt.xlabel('x-coordinates')
    plt.ylabel('y-coordinates')
    plt.legend()

    plt.show()

    return 

def get_avg_dist(T, T_c, i):
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
    with open('approach1_avg_dists_eps_{}.txt'.format(i), 'w') as file1:
        file1.writelines(L)
    return avg_dists

if __name__=="__main__":
    data = import_data.import_data(fn)
    ids = import_data.import_ids(t_ids) 
    traj_dict = import_data.get_traj(data) # this contains ALL of the trajectories
    
    ### simplify results 0.03 0.1 0.3 
    eps = [0.03, 0.1, 0.3]
    for i in range(3):
        ids_from_txt = {key: simplify.simplify_trajectory(traj_dict[key], eps[i]) for key in traj_dict if key in ids} # dictionary list comprehension to filter for just the ones from the txt file
        T_c = approach1(list(ids_from_txt.values()))
        get_avg_dist(ids_from_txt.keys(), T_c, i)
