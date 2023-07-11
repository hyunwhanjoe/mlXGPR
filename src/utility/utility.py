import pickle as pkl
import csv

import numpy as np
from sklearn import preprocessing

"""
This function assumes that there are 3650 enzymatic reactions
"""
def read_data(X_path, y_path, y_type, binarize=False):
    with open(X_path, 'rb') as X_file, open(y_path, 'rb') as y_file:
        X = np.load(X_file, allow_pickle=False)
        y = np.load(y_file, allow_pickle=False)
        y = y.astype(y_type)
        
        if binarize:
            print('abundance binarized')
            preprocessing.binarize(X[:, :3650], copy=False)
        
        return X, y
        

def save_pickle(data, file_name):
    with open(file_name, 'wb') as f:
        return pkl.dump(data,f)
        
def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pkl.load(f)
        
def load_csvindex(csv_file, key, value):
    index = {}
    with open(csv_file, newline='') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            index[row[key]] = row[value]
    
    return index