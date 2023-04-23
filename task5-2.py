"""
Created on 4/20/23

@author: noanir
"""

import task4
import random
from approach1 import dtw
import import_data
import csv
import simplify

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
           idx = random.randint(0, n-1)
           if lst[idx -1] not in group:
               group.append(lst[idx])
       groups.append(group)
       lst = [x for x in lst if x not in group]
       n -= len(group)
   #print([x[:10] for x in groups])
   return groups

def prop_seed(all, k):
   centers = []
   groups = split_into_k_groups(list(all.keys()), k) #returns list of length k, with ids
   #print(groups)
   for group in groups:
       print('Hi')
       avg = task4.approach2(group)
       center = []
       min_dist = float('inf')
       for traj in group:
           print("in this loop")
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
    if seed=="random":
        centers = random.sample(list(T.keys()),k)
    if seed=="proposed":
        centers = prop_seed(T, k)
        

    for numIteration in range(tmax): #for every iteration of Loyd's algorithm
        #list of k clusters 
        clusters = [[] for _ in range(k)] #each [] inside represent a cluster 
        for t in T.keys(): #for every trajectory
            traj_pts = T.get(t)
            distance = float('inf')
            clusterNum = k
            for ct in centers: 
                ct_pts = T.get(ct)
                if dtw(traj_pts, ct_pts)<distance: #calculate the distance between trajectory and a center trajectory
                    distance = dtw(traj_pts, ct_pts) #update distance with minimum distance
                    clusterNum = centers.index(ct) #clusterNum is the index of which that center trajectory appears in "centers"
            clusters[clusterNum].append(t) #put that trajectory into the appropriate cluster
            #so for example clusters[2] has all trajectories in T that is closest to the center trajectory indexed at 2 in "centers"
        
        thresh = 2 # initialize thresh variable TODO fill in
        new_centers=[] 
        for i in range(len(clusters)): #for every cluster (here len(clusters)=k)
            distance = float('inf')
            newCenterTrajectory = task4.approach2(clusters[i]) #calculate the center trajectory for each cluster or group of trajectories
            for c in clusters[i]: #because currently the newCenterTrajectory isn't actually one of the existing trajectories
                c_pts = T.get(c)
                distance2 = dtw(c_pts,T.get(newCenterTrajectory))
                if distance2 < distance:
                    newCenterTrajectory = c
                    distance = distance2 #we need to update the newCenterTrajectory with an existing trajectory in clusters that's closest to the one calculated using approach 2
            new_centers.append(newCenterTrajectory)
        #if for all the distance between the new center trajectory and the previous center trajectory is below a threshold
        #break and return the clusters, else continue regrouping the clusters
        if all(dtw(T.get(new_centers[i]), T.get(centers[i])) < thresh for i in range(k)): #here we assume the index ordering was maintained
            break
        centers = new_centers
        return
        #TO DO: define threshold, define tmax

if __name__ == '__main__':
   data = import_data.import_data(fn)
   ids = import_data.import_ids(t_ids)
   T = get_traj(data)
   k = 5
   seed = 'random'

   ### simplify results 0.03 0.1 0.3
   ids_from_txt = {key: simplify.simplify_trajectory(T[key], 0.3) for key in T if key in ids} # dictionary list comprehension to filter for just the ones from the txt file
   print(k_means_clustering(T, k, seed))
