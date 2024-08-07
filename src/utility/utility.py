import pickle as pkl
import csv

import numpy as np
from sklearn import preprocessing

"""
This function assumes that there are 3650 enzymatic reactions
"""
def read_data(X_path, y_path, y_type, binarize=False, ab_only=False, n_ecs=3650):
    print(X_path)
    print(y_path)
    with open(X_path, 'rb') as X_file, open(y_path, 'rb') as y_file:
        X = np.load(X_file, allow_pickle=False)
        y = np.load(y_file, allow_pickle=False)
        y = y.astype(y_type)
        
        if binarize:
            print('abundance binarized')
            preprocessing.binarize(X[:, :n_ecs], copy=False)
        
        if ab_only:
            print('abundance only')
            X = X[:,:n_ecs]
        
        return X, y
        

def save_np(f_path, obj):
    with open(f_path, 'wb') as f:
        np.save(f, obj, allow_pickle=False)

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

def read_arrayfile_to_list(name):
    l = list()
    with open(name, "r") as f:
        for line in f:
            if line != '':
                l.append(int(line))
    return l
    
def write_array_to_file(file_name, a):
    with open(file_name, "w") as f:
        for value in a:
            f.write(str(value)+'\n')