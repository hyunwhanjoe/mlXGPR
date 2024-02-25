import pickle as pkl

import sys
sys.path.append('../utility')
from utility import load_csvindex
from make_dataset import Dataset

ds = Dataset()
ds.data_path = '../../data'
ds.n_samples = 6
n_ecs = 3650
n_res = 68 # reaction evidence
ds.n_dims = n_ecs + n_res
ds.pwlabel_idx = load_csvindex('../../references/idx_pw.csv', 'Pathway', 'index')
ds.n_pws = len(ds.pwlabel_idx)

X = ds.transform_X_file('/raw/gold_dataset_ptw_ec_63_X.pkl')
ds.save_file(X, '/processed/gold_dataset_6_X.npy')

y = ds.transform_y_file('/raw/gold_dataset_ptw_ec_63_y.pkl')
ds.save_file(y, '/processed/gold_dataset_6_y.npy')
