from pathlib import Path

from evaluate_mlxgpr import evaluate_model
import sys
sys.path.append('../utility')
from utility import read_data, load_pickle

data_path = Path('../../data/processed')
y_type = 'int64'
gold_X = data_path/'gold_dataset_6_X.npy'
gold_y = data_path/'gold_dataset_6_y.npy'

model_name = 'mlXGPR_Chain.pkl'
# model_name = 'mlXGPR_RankChain.pkl'

gold_X, gold_y = read_data(gold_X, gold_y, y_type, ab_only=True)

model_path = Path('../../models')
clf = load_pickle(model_path/model_name)
evaluate_model(clf, gold_X, gold_y)