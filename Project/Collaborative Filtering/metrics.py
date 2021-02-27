from collections import OrderedDict
from collections import namedtuple
import numpy as np

"""
	Taken from sk-learn
"""

def r_precision(targets, preds):
	target_set = set(targets)
	target_count = len(target_set)
	return float(len(set(preds[:target_count]).intersection(target_set))) / target_count

def __get_unique(original_list):
    return list(OrderedDict.fromkeys(original_list))

def dcg(targets, preds, k):
    preds = __get_unique(preds)
    targets = __get_unique(targets)
    if len(preds) == 0 or len(targets) == 0:
        return 0.0
    score = [float(el in targets) for el in preds]
    return np.sum(score / np.log2(1 + np.arange(1, len(score) + 1)))

def ndcg(targets, preds, k):
    idcg = dcg(targets, targets, min(k, len(targets)))
    if idcg == 0:
        raise ValueError("relevent_elements is empty, the metric is"
                         "not defined")
    true_dcg = dcg(targets, preds, k)
    return true_dcg / idcg

def playlist_extender_clicks(targets, preds, k):
    i = set(preds).intersection(set(targets))
    for index, t in enumerate(preds):
        for track in i:
            if t == track:
                return float(int(index / 10))
    return float(k / 10.0 + 1)

def get_avg_scores(target_mat, pred_mat):
	rp_list= []
	dcg_list= []
	click_list= []

	for i in range(target_mat.shape[0]):
		targets= target_mat[i]
		targets= targets[targets!='0']
		preds= pred_mat[i]

		rp_list.append(r_precision(targets,preds))
		dcg_list.append(ndcg(targets,preds,500))
		click_list.append(playlist_extender_clicks(targets,preds,500))

	return np.mean(rp_list), np.mean(dcg_list), np.mean(click_list)