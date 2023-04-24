"""
experiments for task 2
"""

import simplify
import import_data

filename = 'data/geolife-cars-upd8.csv'
trajectories = ['115-20080527225031',
'115-20080528230807',
'115-20080618225237']

def main(T):
    """
    input: original input trajectory T 
    """
    T_star = simplify.simplify_trajectory(T, 0.3)
    return (len(T)/len(T_star))

if __name__ == "__main__":
    data = import_data.import_data(filename)
    T = import_data.get_traj(data)
    results = []
    file2 = open('simplify_tests.txt', 'w')
    for i in range(3):
        t = T.get(trajectories[i])
        results.append("Compression ratio for id = {} : {} \n".format(trajectories[i], main(t)))
    file2.writelines(results)
    file2.close()
    print(results)