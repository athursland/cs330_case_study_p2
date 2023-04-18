"""
task 4 case study part 2
alexandra thursland
mike kim 
noa nir 
"""
from parse import import_data
import csv
import math
import random
import heapq
import time
from matplotlib import pyplot as plt

### define global variables
fn = 'data/geolife-cars-upd8.csv'

if __name__=="__main__":
    data = import_data(fn)
    print(data[:10])