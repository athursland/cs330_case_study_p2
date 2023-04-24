"""
Created on 4/20/23

@author: noanir
"""

import random
from approach1 import dtw
import import_data
import csv
import simplify
from matplotlib import pyplot  as plt
import cProfile

# vars
fn = 'data/geolife-cars-upd8.csv'
t_ids = 'data/trajectory-ids.txt'
global ids_from_txt

def import_ids(fname):
   ids = []
   with open(fname, newline='', encoding='utf-8') as f:
       reader = csv.reader(f)
       for row in reader:
           ids.append(row[0])
   return ids

ids_from_txt = import_ids(fn)

# process trajectory data
def get_traj(data):
   """
   returns a dict where k = t_id and v = datapoints for given trajectory
   """
   trajectories = {}
   for row in data:
       if row[0] not in trajectories:
           trajectories[row[0]] = []
       trajectories[row[0]].append((row[1], row[2]))
   return trajectories

def split_into_k_groups(lst, k):
   n = len(lst)
   group_size = n // k
   groups = []
   for i in range(k):
       group = []
       while len(group) < group_size:
           idx = random.randint(0, n - 1)
           n -= 1
           group.append(lst[idx])
           lst.remove(idx)
       groups.append(group)
   return groups

def prop_seed(all, k):
   centers = []
   groups = split_into_k_groups(list(all.keys()), k)  # returns list of length k, with ids
   for group in groups:
       avg = approach2(group)
       center = []
       min_dist = float('inf')
       for traj in group:
           dist = dtw(all.get(traj), avg)
           if dist < min_dist:
               min_dist = dist
               center = traj
       centers.append(center)
   return centers

def k_means_clustering(T, k, seed):
   '''
   T: dictionary of trajectories where k=t_id and v=LIST of points that make up the trajectory
   k: # of clusters
   seed: random or proposed
   '''
   tmax = 100
   costs = []

   if seed == "random":
       centers = random.sample(list(T.keys()), k)
   if seed == "proposed":
       centers = prop_seed(T, k)

   for n in range(tmax):
       print('run #: {}'.format(n))  # for every iteration of Lloyd's algorithm
       temp = [] #stores the list of costs -- a list of the distance from each trajectory to its center
       clusters = [[] for _ in range(k)]  # each [] inside represent a cluster
       for t in T.keys():  #for every trajectory
           traj_pts = T.get(t)
           distance = float('inf')
           clusterNum = k
           for ct in centers:
               ct_pts = T.get(ct)
               if dtw(traj_pts, ct_pts) < distance:  # calculate the distance between trajectory and a center trajectory
                   distance = dtw(traj_pts, ct_pts) 
                   clusterNum = centers.index(ct)  # clusterNum is the index of which that center trajectory appears in "centers"
           temp.append(distance)
           clusters[clusterNum].append(t)
       #print(costs)
       costs.append(temp)

       thresh = 2  # initialize thresh variable TODO fill in
       new_centers = []
       for i in range(len(clusters)): 
           distance = float('inf')
           T_clust = {key: T[key] for key in T if key in clusters[i]}
           avg_t = approach2(T_clust)
           
           center = avg_t 
           min_dist = float('inf')
           for t_j in T_clust.items():
                if center is not t_j:
                    dist = dtw(avg_t, t_j[1])
                    if dist < min_dist:
                        min_dist = dist
                        center = t_j[0] # id 

           new_centers.append(center)
       # if for all the distance between the new center trajectory and the previous center trajectory is below a threshold
       # break and return the clusters, else continue regrouping the clusters
       if all(dtw(T.get(new_centers[i]), T.get(centers[i])) < thresh for i in range(k)):  
           break
       centers = new_centers
   
   return [T.get(c) for c in centers], costs

def approach2(T):
   #input: the dictionary
   ### defining our M, i.e. traj with max num pts
   M = 0
   t_lengths = []
   for t in T.items():
       t_n = len(t[1])
       if t_n > M:
           M = t_n
       t_lengths.append(t_n)
       print('t_lengths: ', t_lengths) 
   print('M: ', M)

   T_c = []
   for i in range(M):  # unit of time
       all_x = []
       all_y = []
       for j in range(len(T.values())): # for all the trajectories
           if t_lengths[j] == 0:
               continue
           if i / M <= i / t_lengths[j] < (i + 1) / M:
               all_x.append(list(T.values())[j][i][0])
               all_y.append(list(T.values())[j][i][1])

       x = sum(all_x) / len(all_x)
       y = sum(all_y) / len(all_y)
       T_c.append((x, y))

   return T_c

def average_costs(costs, n):
    """
    costs: list of lists where costs[i][j] = avg cost of jth iteration at ith run of Lloyfs
    report experimental results of cost matrix
    for two seeding methods using proposed k
    """
    ### TODO: propose k
    avgs = []
    for j in range(n):
        run_sum = 0
        for i in range(len(costs)):
            run_sum += costs[i][j]
        avgs.append(run_sum/len(costs))
    return avgs

def visualize_avg_costs(random_avgs, prop_avgs):
    """
    using average_costs function, plot the avg cost of clustering 
    over iterations for both seeding methods using suggested value of k
    """
    iter = [j for j in range(1, len(random_avgs))] # arbitrary
    plt.plot(iter, random_avgs, color = 'r', linewidth = 0.8, marker = '.', label = 'random seeding method')
    plt.plot(iter, prop_avgs, color = 'b', linewidth = 0.8, marker = '.', label = 'proposed seeding method')
    plt.title('Avg cost of clustering over iterations for random vs. proposed seeding methods')
    plt.xlabel('iteration')
    plt.ylabel('average cost of clustering')
    plt.legend()

    plt.savefig('avg_costs_over_iterations.png')
    return

def plot_centers(T, centers):
    """
    input: dictionary of traj, list of keys of center trajectories 
    computed from proposed seeding w/ proposed k
    output: save plot of all center clusters
    w/ different colors distinguishing them 
    """
    get_colors = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    colors = get_colors(len(centers))
    
    all_x_by_c = []
    all_y_by_c = []

    for c_id in centers:
        c = T.get(c_id)
        c_x = [p[0] for p in c]
        c_y = [p[1] for p in c]
        all_x_by_c.append(c_x)
        all_y_by_c.append(c_y)

    for i in range(len(centers)):
        plt.plot(all_x_by_c[i], all_y_by_c[i], color = colors[i], linewidth = 0.7, label = 'cluster {}'.format(i))

    plt.title('Center trajectories computed from proposed seeding with proposed k')
    plt.xlabel('x-coordinates')
    plt.ylabel('y-coordinates')
    plt.legend()

    plt.show()
        
    return 

def evaluate_different_k(T):
    """
    input: list of keys fro dictionary, seed 
    output: line plots of avg cost of clustering 
    for k = [4,6,8,10,12] for given seed
    after testing 3 times for robustness 
    """
    k_vals = [4,6,8,10,12]
    avg_costs_r = []
    avg_costs_prop = []

    # get avg costs for each value of k for random seeding
    for i in range(len(k_vals)):
        print('k-val, random seed: {}'.format(k_vals[i]))
        k_costs = []
        for j in range(3):
            print('run {}...'.format(j))
            _, costs = k_means_clustering(T, k_vals[i], 'random')
            k_costs.append(costs)
        avg_costs_r.append(sum(k_costs)/3)

    # get avg costs for each value of k for prop seeding
    for i in range(len(k_vals)):
        print('k-val, prop seed: {}'.format(k_vals[i]))
        k_costs = []
        for j in range(3):
            print('run {}...'.format(j))
            _, costs = k_means_clustering(T, k_vals[i], 'prop')
            k_costs.append(costs)
        avg_costs_r.append(sum(k_costs)/3)


    # save results to a txt file for random seeding
    L = ["avg cost for k = {}: {}\n".format(k[i], avg_costs_r[i]) for i in range(len(k_vals))]
    with open('avg_costs_seed_random.txt', 'w') as file1:
        file1.writelines(L)

    # save results to a txt file for prop seeding
    L = ["avg cost for k = {}: {}\n".format(k[i], avg_costs_prop[i]) for i in range(len(k_vals))]
    with open('avg_costs_seed_prop.txt', 'w') as file2:
        file2.writelines(L)

    # visualize results
    plt.plot(k_vals, avg_costs_r, color = 'r', linewidth = 1, marker = '.', label = 'avg costs of clustering, random seeding')
    plt.plot(k_vals, avg_costs_prop, color = 'b', linewidth = 1, marker = '.', label = 'avg costs of clustering, proposed seeding')
    plt.title('Avg cost of clustering vs. k for both seeding methods')
    plt.xlabel('k-value')
    plt.ylabel('avg cost of clustering')
    plt.legend()
    plt.savefig('avg_costs_vs_k.png')
    
    return

def approach1(trajectories): #trajectories is a list of t-ids
  min_dist = float('inf')
  center = None
  for t_i in trajectories:
      total_distance = 0
      for t_j in trajectories:
          if t_i is not t_j:
              total_distance += dtw(T.get(t_i), T.get(t_j))
      if total_distance < min_dist:
          min_dist = total_distance
          center = t_i
  return center

if __name__ == '__main__':
   data = import_data.import_data(fn)
   #ids = import_data.import_ids(t_ids)
   T_complex = get_traj(data)
   T = {key: simplify.simplify_trajectory(T_complex[key], 0.3) for key in T_complex} # simplified trajectories with eps = 0.3
   n = len(list(T.keys()))
   k = 5 # TODO: update
   #seed = 'random'

    ### identify bottlenecks
   #cProfile.run('approach1(list(T.keys()))')

   ### experiments - evaluate different ks 
   evaluate_different_k(T)

   ######## plot the centers for our proposed k and proposed seeding
   #random_centers, random_costs = k_means_clustering(list(T.keys()), k, 'random')
   #prop_centers, prop_costs = k_means_clustering(list(T.keys()), k, 'proposed')
   #plot_centers(T, prop_centers)

   ######## evaluate averages
   # random_avgs = average_costs(random_costs, len(random_costs))
   # prop_avgs = average_costs(prop_costs, len(prop_costs))
   # visualize_avg_costs(random, prop_avgs)

   
