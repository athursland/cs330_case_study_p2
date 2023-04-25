"""
Created on 4/20/23

@author: noanir
alithursland
mike kim
"""
import time 
import random
from approach1 import dtw
import import_data
import simplify
from matplotlib import pyplot  as plt

# vars
fn = 'data/geolife-cars-upd8.csv'

# process trajectory data
def get_traj(data):
   """
   input: list of trajectories (which are lists of tuples)
   output: a dict where k = t_id and v = datapoints for given trajectory
   """
   trajectories = {}
   for row in data:
       if row[0] not in trajectories:
           trajectories[row[0]] = []
       trajectories[row[0]].append((row[1], row[2]))
   return trajectories

def prop_seed(all, k):
   """
   input: a dictionary where k,v = trajectory_id (str), trajectory (list of int tuples) and an integer k (numer of clusters) 
   output: a list of trajectory ids representing the initial cluster centers
   """
   center_ids = [random.choice(list(all.keys()))]
   while len(center_ids) < k:
       max_distance = 0
       new_center_id = None
       for traj_id in all.keys():
           if traj_id not in center_ids:
               distance = 0
               for c_id in center_ids:
                   traj1 = all[traj_id]
                   traj2 = all[c_id]
                   distance += dtw(traj1, traj2)
               if distance > max_distance:
                   max_distance = distance
                   new_center_id = traj_id
       center_ids.append(new_center_id)
   centers = [traj_id for traj_id in center_ids]
   return centers

def k_means_clustering(T, k, seed):
   '''
   input - T: dictionary of trajectories where k=t_id and v=LIST of points that make up the trajectory
   input - k: # of clusters
   input - seed: random or proposed
   output: list of trajectories in centers, list of average costs 
   '''
   tmax = 100
   costs = []

   if seed == "random":
       centers = random.sample(list(T.keys()), k)
   if seed == "proposed":
       centers = prop_seed(T, k)

   for n in range(tmax):
       print('k-means run #: {}'.format(n)) 
       temp = [] #stores the list of costs -- a list of the distance from each trajectory to its center
       clusters = [[] for _ in range(k)]  # each [] inside represent a cluster
       for t in T.keys():
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
       costs.append(temp)

       thresh = 2  
       new_centers = []
       for i in range(len(clusters)): 
           distance = float('inf')
           T_clust = {key: T[key] for key in T if key in clusters[i]}
           avg_t = approach2(T_clust)
           
           center = avg_t 
           min_dist = float('inf')
           for t_j in T_clust.items():
                if center is not t_j:
                    #print('dtw')
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
    """
    input: T, a dictionary of k,v pairs where k = trajectory_id, v = trajectory as list of int tuples 
    output: the center trajectory (as a list of int tuples)
    """
    #input: the ENTIRE dictionary
    ### defining our M, i.e. traj with max num pts
    M = 0
    t_lengths = []
    for t in T.items():
        t_n = len(t[1])
        if t_n > M:
            M = t_n
        t_lengths.append(t_n)

    T_c = []
    for i in range(M):  # unit of time
        all_x = []
        all_y = []
        for j in range(len(T.values())):
            if t_lengths[j] == 0:
                continue
            if i / M <= i / t_lengths[j] < (i + 1) / M:
                all_x.append(list(T.values())[j][i][0])
                all_y.append(list(T.values())[j][i][1])

        x = sum(all_x) / len(all_x)
        y = sum(all_y) / len(all_y)
        T_c.append((x, y))

    return T_c

def average_costs(costs):
    """
    input - costs: list of lists where costs[i][j] = avg cost of jth iteration at ith run of Lloyds, n = # iterations
    output: list of average costs C_j for all j iterations
    """
    
    avgs = []
    for i in range(0, len(costs)): # for all runs
        run_sum = []
        for j in range(0, len(costs[i])): # over all runs for a specific iteration
            run_sum.append(costs[i][j])
        avgs.append(sum(run_sum)/len(run_sum)) # append avg over all runs for a specific iteration
    return avgs

def visualize_avg_costs(random_avgs, prop_avgs):
    """
    using average_costs function, plot the avg cost of clustering 
    over iterations for both seeding methods using suggested value of k
    """
    iter_r = [j for j in range(len(random_avgs))]
    iter_p = [j for j in range(len(prop_avgs))]
    plt.plot(iter_r, random_avgs, color = 'r', linewidth = 0.8, marker = '.', label = 'random seeding method')
    plt.plot(iter_p, prop_avgs, color = 'b', linewidth = 0.8, marker = '.', label = 'proposed seeding method')
    plt.title('Avg cost of clustering over iterations for random vs. proposed seeding methods')
    plt.xlabel('iteration')
    plt.ylabel('average cost of clustering')
    plt.legend()

    plt.savefig('avg_costs_over_iterations.png')
    return

def plot_centers(centers):
    """
    input: centers = list of center trajectory IDs 
    computed from proposed seeding w/ proposed k
    output: save plot of all center clusters w/ different colors distinguishing them 
    """
    get_colors = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    colors = get_colors(len(centers))
    
    all_x_by_c = []
    all_y_by_c = []

    for c in centers:
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
    input: dictionary of trajectories where k,v = t_id, trajectory as list of int tuple s
    output: line plots of avg cost of clustering 
    for k = [4,6,8,10,12] for given seed
    after testing 3 times for robustness 
    """
    k_vals = [4,6,8,10,12]
    avg_costs_r = []
    avg_costs_prop = []

    start = time.time()
    # get avg costs for each value of k for prop seeding
    for i in range(len(k_vals)):
        k_start = time.time()
        print('k-val, prop seed: {}'.format(k_vals[i]))
        k_costs = []
        for j in range(3):
            print('evaluate func run {}...'.format((j+1)))
            _, costs = k_means_clustering(T, k_vals[i], 'proposed')
            j_cost = []
            for k in costs:
                j_cost.append(sum(k)/len(k)) ### avg for this iteration
            k_costs.append(sum(j_cost)/len(j_cost)) ### avg for this entire run 
        avg_costs_prop.append(sum(k_costs)/3) ## avg over 3 runs, append to final list, idx == value of k
        k_end = time.time()
        print('Time elapsed for k = {}: {}'.format(str(k[i]), str(k_end - k_start)))
    end = time.time()
    print('Time elapsed for prop seeding: ', str(end - start))
    
    start = time.time()
    # get avg costs for each value of k for random seeding
    for i in range(len(k_vals)):
        k_start = time.time()
        print('k-val, random seed: {}'.format(k_vals[i]))
        k_costs = []
        for j in range(3):
            print('evaluate func run {}...'.format((j+1)))
            _, costs = k_means_clustering(T, k_vals[i], 'random')
            j_cost = []
            for k in costs:
                j_cost.append(sum(k)/len(k)) ### avg for this iteration
            k_costs.append(sum(j_cost)/len(j_cost)) 
        avg_costs_r.append(sum(k_costs)/3) ## avg over 3 runs
        k_end = time.time()
        print('Time elapsed for k = {}: {}'.format(str(k[i]), str(k_end - k_start)))
    end = time.time()
    print('Time elapsed for random seeding: ', str(end - start))

    # save results to a txt file for random seeding
    L = ["avg cost for k = {}: {}\n".format(str(k[i]), str(avg_costs_r[i])) for i in range(len(k_vals))]
    with open('avg_costs_seed_random.txt', 'w') as file1:
        file1.writelines(L)

    # save results to a txt file for prop seeding
    L = ["avg cost for k = {}: {}\n".format(str(k[i]), str(avg_costs_prop[i])) for i in range(len(k_vals))]
    with open('avg_costs_seed_prop.txt', 'w') as file2:
        file2.writelines(L)
    
    # visualize results
    plt.plot(k_vals, avg_costs_r, color = 'r', linewidth = 1, marker = '.', label = 'avg costs of clustering, random seeding')
    plt.plot(k_vals, avg_costs_prop, color = 'b', linewidth = 1, marker = '.', label = 'avg costs of clustering, proposed seeding')
    plt.title('Avg cost of clustering vs. k for both seeding methods')
    plt.xlabel('k-value')
    plt.ylabel('avg cost of clustering')
    plt.legend()
    plt.savefig('avg_costs_vs_k_2.png')
    
    return

if __name__ == '__main__':
   data = import_data.import_data(fn)
   T_complex = get_traj(data)
   T = {key: simplify.simplify_trajectory(T_complex[key], 0.3) for key in T_complex} # simplified trajectories with eps = 0.3
   n = len(list(T.keys()))
   k = 10

   ######## experiments - evaluate different ks 
   evaluate_different_k(T)

   ######## experiments - plot the centers for our proposed k and proposed seeding
   random_centers, random_costs = k_means_clustering(T, k, 'random')
   prop_centers, prop_costs = k_means_clustering(T, k, 'proposed')
   plot_centers(prop_centers)

   ######## experiments - evaluate averages
   random_avgs = average_costs(random_costs)
   prop_avgs = average_costs(prop_costs)
   visualize_avg_costs(random_avgs, prop_avgs)

   
