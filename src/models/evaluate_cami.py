from pathlib import Path
import csv
import sys
sys.path.append('../utility')
from utility import read_data, load_pickle

import xgboost as xgb
from sklearn.metrics import f1_score, precision_score,\
                            recall_score, hamming_loss

def evaluate_model(clf, X, y):
    y_hat = clf.predict(X)
    
    h = f'{hamming_loss(y, y_hat):.4f}'
    p = f'{precision_score(y, y_hat, average="samples"):.4f}'
    r = f'{recall_score(y, y_hat, average="samples"):.4f}'
    f1 = f'{f1_score(y, y_hat, average="samples"):.4f}'

    with open('cami.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['hamming', h])
        csvwriter.writerow(['prec', p])
        csvwriter.writerow(['recall', r])
        csvwriter.writerow(['f1', f1])

data_path = '../../data/processed/'
y_type = 'int64'
X = data_path+'cami_X.npy'
y = data_path+'cami_y.npy'
X, y = read_data(X, y, y_type, ab_only=True)

model_name = 'mlXGPR_RankChain.pkl'
# model_name = 'mlXGPR_RankChain_Biocyc.pkl'

model_path = Path('../../models')
clf = load_pickle(model_path/model_name)
evaluate_model(clf, X, y)