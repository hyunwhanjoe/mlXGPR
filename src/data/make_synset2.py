import time

import pickle as pkl
import csv
import numpy as np
import scipy

import sys
sys.path.append('../utility')
from utility import load_csvindex

class Dataset:
    def __init__(self):
        self.data_path = ''
        self.n_dims = ''
        self.pwlabel_idx = ''
        self.n_samples = ''
        self.n_pws = ''

#  https://github.com/hallamlab/mlLGPR/blob/master/src/model/mlLGPR.py
    def transform_X_file(self, X_file):
        start = time.perf_counter()
        X = np.zeros((self.n_samples, self.n_dims), dtype=np.float64)
        start_idx = 0
        
        with open(self.data_path+X_file, 'rb') as f_x_in:
            while start_idx < self.n_samples:
                try:
                    tmp = pkl.load(f_x_in)
                    if type(tmp) is scipy.sparse._lil.lil_matrix:
                        tmp = tmp.toarray()
                    
                    if type(tmp) is np.ndarray:
                        X[start_idx] = tmp[0,:self.n_dims]
                        
                        if (start_idx == 0) or (start_idx == self.n_samples-1):
                            assert np.array_equal(X[start_idx], tmp[0,:self.n_dims])
                            assert X[start_idx,0] == tmp[0,0]
                            assert X[start_idx,-1] == tmp[0,self.n_dims-1]
                        
                        start_idx += 1
                    else:
                        continue
                except IOError:
                    break
        end = time.perf_counter()
        print(f'transform_X_file took {(end - start):.4f} seconds')
        
        return X
    
    def transform_y_file(self, y_file):
        start = time.perf_counter()
        def present_pws(pws):
            return [int(self.pwlabel_idx[pw]) for pw in pws]
            
        with open(self.data_path+y_file, 'rb') as f_y_in:
            tmp = pkl.load(f_y_in)
            
            if type(tmp) is str: # comment
                tmp = pkl.load(f_y_in)
            
            if type(tmp) is tuple:
                y = np.zeros((self.n_samples, self.n_pws), dtype=np.int8)
                for i in range(self.n_samples):
                    pws = present_pws(tmp[0][i])
                    y[i, pws] = 1
            
            if type(tmp) is scipy.sparse._lil.lil_matrix:
                y = tmp.toarray().astype(np.int8)
            
            end = time.perf_counter()
            print(f'transform_y_file took {(end - start):.4f} seconds')
            
            return y
    
    def save_file(self, obj, filename):
        with open(self.data_path+filename, 'wb') as f:
            np.save(f, obj, allow_pickle=False)
            


if __name__ == "__main__":
    ds = Dataset()
    ds.data_path = '../../data'
    ds.n_samples = 15000
    n_ecs = 3650
    n_res = 68 # reaction evidence
    ds.n_dims = n_ecs + n_res
    ds.pwlabel_idx = load_csvindex('../../references/idx_pw.csv', 'Pathway', 'index')
    ds.n_pws = len(ds.pwlabel_idx)
    
    X = ds.transform_X_file('/raw/syn_dataset_ptw_ec_15000_X_noise.pkl')
    ds.save_file(X, '/processed/Synset-2_X.npy')

    y = ds.transform_y_file('/raw/syn_dataset_ptw_ec_15000_y_noise.pkl')
    ds.save_file(y, '/processed/Synset-2_y.npy')