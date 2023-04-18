"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""

import csv
import math
import random
import heapq
import time
from matplotlib import pyplot as plt

### define global variables
fn = 'data/geolife-cars-upd8.csv'

data = []
grid = None

def import_data(fname):
    global data

    with open(fname, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None) # skip the headers
        for row in reader:
            id = row[0]
            x = float(row[1])
            y = float(row[2])
            data.append((id, x, y))

if __name__=="__main__":
    import_data(fn)
    print(data[:10])