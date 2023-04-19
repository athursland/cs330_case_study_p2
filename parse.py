"""
import data module
with id, x, y coords
"""
import csv

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