"""
Created on 4/20/23

@author: noanir
"""

import task4
import random
from task4 import dtw
from parse import import_data
import csv

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

def k_means_clustering(T, k, seed):
    '''
    T: dictionary of trajectories where k=t_id and v=LIST of points that make up the trajectory
    k: # of clusters
    seed: random or proposed
    '''
    tmax = 100
    if seed=="random":
        centers = random.sample(T.values(),k) #returns k random trajectories from T
    if seed=="proposed":
        #TO DO: choose the centers in a more meaningful way
        pass

    for numIteration in range(tmax): #for every iteration of Loyd's algorithm
        #list of k clusters 
        clusters = [[] for _ in range(k)] #each [] inside represent a cluster 
        for trajectory in T.values(): #for every trajectory
            distance = float('inf')
            clusterNum = k
            for ct in centers: 
                if dtw(trajectory,ct)<distance: #calculate the distance between trajectory and a center trajectory
                    distance = dtw(trajectory,ct) #update distance with minimum distance
                    clusterNum = centers.index(ct) #clusterNum is the index of which that center trajectory appears in "centers"
            clusters[clusterNum].append(trajectory) #put that trajectory into the appropriate cluster
            #so for example clusters[2] has all trajectories in T that is closest to the center trajectory indexed at 2 in "centers"
        
        thresh = 2 # initialize thresh variable TODO fill in
        new_centers=[] 
        for i in range(len(clusters)): #for every cluster (here len(clusters)=k)
            newCenterTrajectory = task4.approach2(clusters[i]) #calculate the center trajectory for each cluster or group of trajectories
            for c in clusters[i]: #because currently the newCenterTrajectory isn't actually one of the existing trajectories
                distance2 = dtw(c,newCenterTrajectory)
                if dtw(c,newCenterTrajectory)<distance2:
                    newCenterTrajectory = c #we need to update the newCenterTrajectory with an existing trajectory in clusters that's closest to the one calculated using approach 2
            new_centers.append(newCenterTrajectory)
        #if for all the distance between the new center trajectory and the previous center trajectory is below a threshold
        #break and return the clusters, else continue regrouping the clusters
        if all(dtw(new_centers[i],centers[i]) < thresh for i in range(k)): #here we assume the index ordering was maintained
            break
        centers = new_centers 
        return
        #TO DO: define threshold, define tmax

if __name__ == '__main__':
   data = import_data(fn)  # this is fine
   #ids = import_ids(t_ids)  # this is also fine
   T = get_traj(data)  ###### NOT FINE
   k = 5
   seed = 'random'
   print(k_means_clustering(T, k, seed))
   #print(T.values())
