import numpy as np
import pandas as pd
from metrics import *
from parameters import *

def evaluate():
	pred_dataset= pd.read_csv(FILES_PATH+'test_preds.csv', header=None)
	target_dataset= pd.read_csv(FILES_PATH+'test_targets.csv', header=None, dtype=str)

	rp, ndcg, clicks= get_avg_scores(pred_dataset.drop(0).to_numpy(), target_dataset.drop(0).to_numpy())

	print("rp= ", rp)
	print("ndcg= ", ndcg)
	print("clicks= ", clicks)

evaluate()
