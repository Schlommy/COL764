import pickle
import pandas as pd
import scipy.sparse as sp
import numpy as np
from parameters import *


tracks_df= pd.read_csv(FILES_PATH+'tracks.csv')

def bm25_normalize(mat):
	df_list= np.ravel(mat.sum(axis=1))
	pickle.dump(df_list, open(FILES_PATH+'df_list.pkl','wb'))
	doc_lens= np.ravel(mat.sum(axis=0))
	doc_lens_avg= int(np.mean(doc_lens))
	print(doc_lens_avg)
	mat.data= np.log2(n_docs/(1+df_list[mat.row]))*mat.data*(k1+1)/(k1*((1-b)+b*(doc_lens[mat.col]/doc_lens_avg))+mat.data)
	return mat

def get_tvp_matrix():
	playlist_df= pd.read_csv(FILES_PATH+'playlists.csv').iloc[:-5000]
	n_rows= len(playlist_df)
	n_cols= n_tracks

	row_vals= []
	col_vals= []

	for pid in playlist_df.index:
		for tid in playlist_df.tracks[pid][1:-1].split(', '):
			row_vals.append(pid)
			col_vals.append(int(tid))

	tvp_matrix= sp.coo_matrix((np.ones(len(row_vals)), (row_vals, col_vals)), shape=(n_rows,n_cols))
	tvp_matrix= tvp_matrix.getH()
	tvp_matrix= bm25_normalize(tvp_matrix)

	return tvp_matrix

def get_sim_matrix(tvp_matrix):
	sim_matrix= tvp_matrix.dot(tvp_matrix.getH())
	return sim_matrix

tvp_matrix= get_tvp_matrix()
sim_matrix= get_sim_matrix(tvp_matrix)
#tvp_matrix= sp.csc_matrix(tvp_matrix)

sp.save_npz(FILES_PATH+'tvp_matrix.npz', tvp_matrix)
sp.save_npz(FILES_PATH+'sim_matrix.npz', sim_matrix)
