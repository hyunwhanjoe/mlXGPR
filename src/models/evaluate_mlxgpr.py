from pathlib import Path
import time
import csv

from sklearn.metrics import f1_score, precision_score,\
                            recall_score, hamming_loss

import numpy as np
import xgboost as xgb

import sys
sys.path.append('../utility')
from utility import read_data

def evaluate_model(clf, gold_X, gold_y, early_stop=False):
    gold_pgdbs = ['AraCyc', 'EcoCyc', 'HumanCyc', 'LeishCyc', 'TrypanoCyc', 'YeastCyc']
    order = ['EcoCyc', 'HumanCyc', 'AraCyc', 'YeastCyc', 'LeishCyc', 'TrypanoCyc']
    hamms=[]
    precs = []
    recalls = []
    f1s = []
    
    if early_stop:
        Y_hat = clf.predict(gold_X, iteration_range=(0, clf.best_iteration+1))
    else:
        Y_hat = clf.predict(gold_X)
    
    for i in range(len(gold_pgdbs)):
        y = gold_y[i]
        y_hat = Y_hat[i]
        
        hamms.append(f'{hamming_loss(y, y_hat):.4f}')
        precs.append(f'{precision_score(y, y_hat):.4f}')
        recalls.append(f'{recall_score(y, y_hat):.4f}')
        f1s.append(f'{f1_score(y, y_hat):.4f}')
        
    def reorder():
        pgdb_map = {pgdb:i for i, pgdb in enumerate(gold_pgdbs)}
        
        reordered_hamms = [hamms[pgdb_map[pgdb]] for pgdb in order]
        reordered_precs = [precs[pgdb_map[pgdb]] for pgdb in order]
        reordered_recalls = [recalls[pgdb_map[pgdb]] for pgdb in order]
        reordered_f1s = [f1s[pgdb_map[pgdb]] for pgdb in order]
        
        return reordered_hamms, reordered_precs,\
                reordered_recalls, reordered_f1s
    
    def write_results(reordered_hamms, reordered_precs,\
                        reordered_recalls, reordered_f1s):
        with open('biocyc.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', 
                                    quoting=csv.QUOTE_MINIMAL)
            
            order.insert(0,'metrics')
            reordered_hamms.insert(0,'hamming')
            reordered_precs.insert(0,'prec')
            reordered_recalls.insert(0,'recall')
            reordered_f1s.insert(0,'f1')
            
            csvwriter.writerow(order)
            csvwriter.writerow(reordered_hamms)
            csvwriter.writerow(reordered_precs)
            csvwriter.writerow(reordered_recalls)
            csvwriter.writerow(reordered_f1s)
    
    reordered_hamms, reordered_precs, reordered_recalls, reordered_f1s=reorder()
    write_results(reordered_hamms, reordered_precs, reordered_recalls, reordered_f1s)

if __name__ == '__main__':
    data_path = Path('../../data/processed')
    y_type = 'int64'
    gold_X = data_path/'gold_dataset_6_X.npy'
    gold_y = data_path/'gold_dataset_6_y.npy'
    
    model_name = 'mlXGPR_AB.json'
    gold_X, gold_y = read_data(gold_X, gold_y, y_type, ab_only=True)
    
    # model_name = 'mlXGPR_AB_RE.json'
    # gold_X, gold_y = read_data(gold_X, gold_y, y_type)
    
    clf = xgb.XGBClassifier()
    model_path = Path('../../models')
    clf.load_model(model_path/model_name)
    
    evaluate_model(clf, gold_X, gold_y)