from dbscanner import *
import csv

rawDataPath = "F:\\your\\raw\\data\path.csv"


def main(rawDataPath):
    [Data, eps, MinPts] = getData(rawDataPath)
    dbc = dbscanner()
    dbc.dbscan(Data, eps, MinPts, rawDataPath)


def getData(rawDataPath):
    # retrieve related data
    Data = []
    with open(rawDataPath, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            Data.append([float(row[3]), float(row[4])])  # row3: latitude  row4: longitude
        f.flush()
        f.close()
    return [Data, 0.0001, 20]
