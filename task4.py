"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""
import import_data
import approach1
import simplify
from matplotlib import pyplot as plt
import random

### define global variables
fn = 'data/geolife-cars-upd8.csv'
t_ids = 'data/trajectory-ids.txt'
global ids
global ids_from_txt

#################
##### APPROACH 2
#################

def approach2(T):
    """
    input: keys from the dictionary
    """
    ### defining our M, i.e. traj with max num pts 
    M = 0
    t_lengths = []
    for t in T:
        t_n = len(ids_from_txt.get(t))
        if t_n > M:
            M = t_n
        t_lengths.append(t_n)
    
    T_c = []
    for i in range(M): # unit of time
        all_x = []
        all_y = []
        for j in range(len(T)):
            if i/M <= i/t_lengths[j] < (i+1)/M: 
                # the first LEQ and the last LE ensures that the first and last points 
                # are aligned for every trajectory
                t = ids_from_txt.get(T[j])
                all_x.append(t[i][0])
                all_y.append(t[i][1])
        x = sum(all_x)/len(all_x)
        y = sum(all_y)/len(all_y)
        T_c.append((x,y))

    return T_c

#########################
##### EXPERIMENTS
#########################

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
                d = approach1.dist(t[i], T_c[j])
                if d < closest_d:
                        closest_d = d
            d_sum += closest_d
        avg_dists.append(d_sum/n)

    L = ["avg dist to trajectory {}: {}\n".format(i, avg_dists[i]) for i in range(len(T))]
    with open('approach2_avg_dists.txt', 'w') as file1:
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
        plt.plot(T_x[i], T_y[i], color = colors[i], linewidth = 0.7, alpha = 0.8, label = 'trajectory {}'.format(i))

    plt.plot(T_c_x, T_c_y, color = 'r', linewidth = 0.8, label = 'approach 2 center')
    plt.title('Given trajectories and computed trajectory center')
    plt.xlabel('x-coordinates')
    plt.ylabel('y-coordinates')
    plt.legend()

    plt.show()

    return 

#################
##### MAIN
#################

if __name__=="__main__":
    data = import_data.import_data(fn)
    ids = import_data.import_ids(t_ids) 
    traj_dict = import_data.get_traj(data) # this contains ALL of the trajectories
    ids_from_txt = {key: traj_dict[key] for key in traj_dict if key in ids} # dictionary list comprehension to filter for just the ones from the txt file
    T_c = approach2(list(ids_from_txt.keys()))

    ### simplify results 0.3
    eps = [0.03, 0.1, 0.3]
    for i in range(3):
        ids_from_txt = {key: simplify.simplify_trajectory(traj_dict[key], eps[i]) for key in traj_dict if key in ids} # dictionary list comprehension to filter for just the ones from the txt file
        T_c = approach1(list(ids_from_txt.values()))

    visualize(ids_from_txt.keys(), T_c)
    