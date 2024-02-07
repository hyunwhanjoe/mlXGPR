from pathlib import Path
import time
import csv

import xgboost as xgb
from sklearn.multioutput import ClassifierChain

from train_mlxgpr import log

import sys
sys.path.append('../utility')
from utility import read_data, save_pickle
from utility import read_arrayfile_to_list

data_path = Path('../../data/processed')
y_type = 'int64'
X_path = data_path/'Synset-2_X.npy'
y_path = data_path/'Synset-2_y.npy'

X_train, y_train = read_data(X_path, y_path, y_type, ab_only=True)
n_jobs=35
clf = xgb.XGBClassifier(n_jobs=n_jobs,
                        tree_method='hist',
                        max_depth=4,
                        n_estimators=22)
                        
t0 = time.time()
chain = ClassifierChain(clf)
model_name = 'mlXGPR_Chain.pkl'

# order_file='order.txt'
# order = read_arrayfile_to_list('../../references/'+order_file)
# chain = ClassifierChain(clf, order=order)
# model_name = 'mlXGPR_RankChain.pkl'

chain.fit(X_train, y_train)
t1 = time.time() - t0

log(model_name, t1, n_jobs)
model_path = Path('../../models')
save_pickle(chain, model_path/model_name)
print(model_name)
