import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import xgboost as xgb
import numpy as np

from train_mlxgpr import log

import sys
sys.path.append('../utility')
from utility import read_data
from utility import write_array_to_file

def determine_chain_order(V, G, metric):
    X_valid = V[0]
    
    Y_V = V[1]
    Y_hat_V = G.predict(X_valid)
    
    Y_V_T= Y_V.T
    Y_hat_V_T = Y_hat_V.T
    
    scores = []
    
    t = Y_V_T.shape[0] # of pathways
    for j in range(t):
        score = metric(Y_V_T[j], Y_hat_V_T[j])
        scores.append(score)
    
    pi = np.flip(np.argsort(np.array(scores), kind='stable'))
    return pi


data_path = '../../data/processed/'
y_type = 'int64'
X_path = data_path+'Synset-2_X.npy'
y_path = data_path+'Synset-2_y.npy'

X_train, y_train = read_data(X_path, y_path, y_type, ab_only=True)
X_train, X_valid, y_train, y_valid =\
train_test_split(X_train, y_train, test_size=(1/6), shuffle=False)

model_path = '../../models/'
model_name = 'mlXGPR_AB_split.json'

# n_jobs=35
# clf = xgb.XGBClassifier(n_jobs=n_jobs,
                        # tree_method='hist',
                        # max_depth=4,
                        # n_estimators=22)
# t0 = time.time()
# clf.fit(X_train, y_train)
# t1 = time.time() - t0
# log(model_name, t1, n_jobs)
# clf.save_model(model_path+model_name)

clf = xgb.XGBClassifier()
clf.load_model(model_path+model_name)

order = determine_chain_order((X_valid,y_valid), clf, f1_score)
file_name='order.txt'
write_array_to_file('../../references/'+file_name, order)