"""
Created on 4/20/23

@author: noanir
"""

import random
from task4 import dtw
from parse import import_data

#vars
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

# process trajectory data
def get_traj(data):
   """
   returns a dict where k = t_id and v = datapoints for given trajectory
   """
   trajectories = {}
   for row in data:
      # if row[0] in ids:
       if row[0] not in trajectories:
           trajectories[row] = [(row[1], row[2])]
       else:
           trajectories[row].append((row[1], row[2]))
   return trajectories


def k_means_clustering(T, k, seed):
   """
   Clusters a set of trajectories T into k clusters using Lloyd's algorithm.

   Args:
   - T: a list of trajectories, where each trajectory is a list of points
   - k: the number of clusters to partition T into
   - distance_fn: a function that computes the distance between two trajectories
   - tmax: the maximum number of iterations to run Lloyd's algorithm
   - tol: the tolerance for convergence, defined as the maximum change in cluster assignments between iterations

   Returns:
   - A tuple (centers, assignments, distances), where:
       - centers: a list of k center trajectories, where each center is a list of points
       - assignments: a list of integers of length len(T), indicating the cluster assignment for each trajectory
       - distances: a list of floats of length tmax, indicating the sum of squared distances between each trajectory and its assigned center trajectory at each iteration
   """
   tmax = 100 #should choose to be a function of simplification and k

   # initialize centers using random trajectories from T
   if seed == "r":
       centers = random.sample(T, k) #--> returns k random trajectories from T

   # initialize cluster assignments and distances
   assignments = [0] * len(T)
   distances = [] #--> cost function for each iteration, want to report
   # distances[-1] = total cost for clusters on the last iteration

   # run Lloyd's algorithm
   for t in range(tmax):
       # Center computation: compute the center trajectory for each cluster
       new_centers = []
       for j in range(k):
           Tj = [T[i] for i in range(len(T)) if assignments[i] == j]
           if len(Tj) > 0:
               center = [sum(coord) / len(Tj) for coord in zip(*Tj)]
               new_centers.append(center)
           else:
               new_centers.append(centers[j])

       # Re-assignment: assign each trajectory to the cluster with the closest center trajectory
       new_assignments = [0] * len(T)
       total_distance = 0
       for i in range(len(T)):
           distances_to_centers = [dtw(T[i], center) for center in new_centers]
           closest_center = distances_to_centers.index(min(distances_to_centers))
           new_assignments[i] = closest_center
           total_distance += distances_to_centers[closest_center] ** 2

       # check for convergence
       if assignments == new_assignments:
           break

       # update centers, assignments, and distances
       centers = new_centers
       assignments = new_assignments
       distances.append(total_distance)

       # check for convergence based on change in cluster assignments
       if t > 0 and max([assignments[i] != new_assignments[i] for i in range(len(T))]) == 0:
           break

   return centers, assignments, distances


if __name__ == '__main__':
   data = import_data(fn)  # this is fine
   #ids = import_ids(t_ids)  # this is also fine
   T = get_traj(data)  ###### NOT FINE
   print(T.values())
   # print(T.items())
   #print(approach2(list(T.values())))
