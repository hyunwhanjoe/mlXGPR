from pathlib import Path
import time
import csv

import xgboost as xgb

import sys
sys.path.append('../utility')
from utility import read_data

def log(model_name,t1, n_jobs):
    with open('running_time.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['model_name', 'n_jobs', 'time_s', 'time_m'])
        csvwriter.writerow([model_name, n_jobs, round(t1,1), round(t1/60,2)])

data_path = Path('../../data/processed')
y_type = 'int64'
X_path = data_path/'Synset-2_X.npy'
y_path = data_path/'Synset-2_y.npy'
X_train, y_train = read_data(X_path, y_path, y_type)

n_jobs=10
clf = xgb.XGBClassifier(n_jobs=n_jobs,
                        tree_method='hist',
                        max_depth=4,
                        n_estimators=19)

t0 = time.time()
clf.fit(X_train, y_train)
t1 = time.time() - t0

model_name = 'model.json'
log(model_name, t1, n_jobs)

model_path = Path('../../models')
clf.save_model(model_path/model_name)
print(model_path/model_name)