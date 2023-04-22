"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""
import math
import import_data

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
