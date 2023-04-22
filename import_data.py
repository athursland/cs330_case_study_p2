"""
import data module
with id, x, y coords
"""
import csv

# import data frmo csv 
def import_data(fname):
    data = []
    with open(fname, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None) # skip the headers
        for row in reader:
            id = row[0]
            x = float(row[1])
            y = float(row[2])
            data.append((id, x, y))

    return data

# import trajectory ids from txt file 
def import_ids(fname):
    ids = []
    with open(fname, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ids.append(row[0])

    return ids

# make a dict of all the trajectory ids and their points
def get_traj(data):
    """
    returns a dict where k = t_id and v = datapoints for given trajectory
    """
    trajectories = {}
    for row in data:
        #print(row[0])
        if row[0] not in trajectories:
            trajectories[row[0]] = []
        trajectories[row[0]].append((row[1], row[2]))
    return trajectories

if __name__ == "__main__":
    print(import_ids('geolife-cars-upd8.csv'))