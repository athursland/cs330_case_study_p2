"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""

############################
##### SIMPLIFY TRAJECTORY 
############################

import math
import import_data
distances = {}

def dist(p1, p2):  ### added memoization
    if (p1, p2) in distances:
        return distances[(p1, p2)]
    elif (p2, p1) in distances:
        return distances[(p2, p1)]
    else:
        x1, y1 = p1
        x2, y2 = p2
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        distances[(p1, p2)] = distance
        return distance

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

### modified to use binary search to find the furthest point
def simplify_trajectory(T, eps):
    if len(T) < 3:
       # Base case: return the input trajectory if it has 2 or fewer points
       return []

    T_start=T[0]
    T_end=T[-1]
    max_dist = 0

    left = 1
    right = len(T) - 2
    while left <= right:
        mid = (left + right) // 2
        dist_mid = dist_point_segment(T[mid], (T_start, T_end))
        dist_left = dist_point_segment(T[mid - 1], (T_start, T_end))
        dist_right = dist_point_segment(T[mid + 1], (T_start, T_end))
        if dist_mid > dist_left and dist_mid > dist_right:
            # We have found the furthest point
            max_idx = mid
            max_dist = dist_mid
            break
        elif dist_left > dist_right:
            # furthest point is left 
            right = mid - 1 
        else:  
            # furthest point is right 
            left = mid + 1 
    
    if max_dist > eps:
        # Recursively simplify the trajectory on both sides of the furthest point
        simplified_left = simplify_trajectory(T[:max_idx + 1], eps)
        simplified_right = simplify_trajectory(T[max_idx:], eps)
        return simplified_left[:-1] + simplified_right
    else:
        if len(T) <= eps:
            return
        else:
            return [T[0], T[-1]]


if __name__ == "__main__":
    fn = 'data/geolife-cars-upd8.csv'
    data = import_data.import_data(fn)
    T = import_data.get_traj(data)
    simp = []
    for t in list(T.values()):
        print(simplify_trajectory(t, 0.3))