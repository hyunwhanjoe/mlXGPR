import sys
sys.path.append('../utility')
from utility import read_data
import csv

import xgboost as xgb
from sklearn.metrics import f1_score, precision_score,\
                            recall_score, hamming_loss

def evaluate_model(clf, X, y):
    y_hat = clf.predict(X)

    h = round(hamming_loss(y, y_hat),4)
    p = round(precision_score(y, y_hat, average='samples'),4)
    r = round(recall_score(y, y_hat, average='samples'),4)
    f1 = round(f1_score(y, y_hat, average='samples'),4)

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
X, y = read_data(X, y, y_type)

model_name = 'model.json'
model_path = '../../models/'
clf = xgb.XGBClassifier()
clf.load_model(model_path+model_name)

evaluate_model(clf, X, y)