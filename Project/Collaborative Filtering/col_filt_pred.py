import scipy.sparse as sp
import numpy as np
import pandas as pd
import pickle
from parameters import *

def bm25_normalize(mat):
	df_list= np.ravel(pickle.load(open(FILES_PATH+'df_list.pkl','rb')))
	doc_lens= np.ravel(mat.sum(axis=0))
	mat.data= np.log2(n_docs/(1+df_list[mat.row]))*mat.data*(k1+1)/(k1*((1-b)+b*(doc_lens[mat.col]/doc_lens_avg))+mat.data)
	return mat

def get_col_scores(test_mat):
	sim_matrix= sp.load_npz(FILES_PATH+'sim_matrix.npz')
	test_mat_bm= test_mat.copy()
	test_mat_bm= bm25_normalize(test_mat_bm)

	test_score= sim_matrix.dot(test_mat_bm)

	del sim_matrix

	test_score= test_score.A
	test_score[test_mat_bm.A!=0]= -1

	return test_score