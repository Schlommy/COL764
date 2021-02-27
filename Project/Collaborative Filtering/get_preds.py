import scipy.sparse as sp
import numpy as np
import pandas as pd
import json
import gc
import pickle
from parameters import *
from col_filt_pred import *

def get_test_data():
	test_json= json.load(open(FILES_PATH+"test_dataset.json"))
	tr_uri2id= pickle.load(open(FILES_PATH+'uri2id.pkl','rb'))

	row_vals2= []
	col_vals2= []
	pid_list= []

	i=0
	for plist in test_json["data"]:
		pid_list.append(plist['pid'])
		for track in plist["test_tracks"]:
			col_vals2.append(i)
			row_vals2.append(tr_uri2id[track])       
		i+=1

	n_testplays= len(pid_list)
	test_mat= sp.coo_matrix((np.ones(len(row_vals2)), (row_vals2, col_vals2)), shape=(n_tracks,n_testplays))

	return test_mat, pid_list

def get_total_scores(test_mat):
	col_filt_scores= get_col_scores(test_mat)
	# con_filt_scores= get_con_scores(test_mat)
	# cold_scores= get_cold_scores(test_mat)

	total_scores= col_filt_scores

	return total_scores

def get_ranks(test_mat):
	total_scores= get_total_scores(test_mat)
	test_ranks= total_scores.argsort(axis=0)[::-1][:500,:]
	return test_ranks

test_mat, pid_list= get_test_data()
test_ranks= get_ranks(test_mat)

tracks_df= pd.read_csv(FILES_PATH+'tracks.csv')
uri_dict= tracks_df.track_uri.to_dict()

preds= pd.DataFrame(test_ranks.T)
#preds= preds.applymap(lambda x: tracks_df.iloc[x]['track_uri'])
preds= preds.applymap(lambda x: uri_dict[x])
preds.insert(loc=0, value=pid_list, column='pid')
preds.to_csv(FILES_PATH+'test_preds.csv', index=False, header=False)

