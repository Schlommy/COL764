import pandas as pd
import numpy as np
import json
from parameters import *

np.random.seed(42)
test_cols= ["pid", "name", "num_holdouts", "test_tracks", "target_tracks", "num_tracks", "num_samples"]

def get_list(track_string, low, is_random, tracks_df):
	lst1= []
	lst2= []
	np.random.seed(42)

	tracks= track_string[1:-1].split(', ')
	if is_random:
		np.random.shuffle(tracks)
	for tid in tracks[:low]:
		lst1.append(tracks_df.loc[int(tid),'track_uri'])
	for tid in tracks[low:]:
		lst2.append(tracks_df.loc[int(tid),'track_uri'])
	lst2+= ['0']*(500-len(lst2))

	return [lst1, lst2]

def get_test_data(params):
	tracks_df= pd.read_csv(FILES_PATH+'tracks.csv')
	playlist_df= pd.read_csv(FILES_PATH+'playlists.csv')
	test_df= playlist_df.iloc[-5000:].copy()

	test_dataset= pd.DataFrame(columns= test_cols)

	for param in params:
		num_samples, keep_name, is_random= param
		first= test_df[test_df.num_tracks>num_samples].sample(1000, random_state=1).copy()
		first['num_samples']= num_samples
		first['num_holdouts']= first.num_tracks-first.num_samples
		if keep_name==0:
			first['name']= ''
		first= pd.concat([first, first.apply(lambda x: pd.Series(get_list(x.tracks,num_samples,is_random,tracks_df), index=["test_tracks", "target_tracks"]),axis=1)], axis=1)
		first= first.filter(items= test_cols)
		test_dataset= test_dataset.append(first, ignore_index= True)

	test_targets= test_dataset[['pid','target_tracks']].copy()
	test_targets= test_targets.join(test_targets.apply(lambda x: x.target_tracks, axis=1, result_type='expand'))
	test_dataset.drop(columns=['target_tracks'], inplace=True)
	test_targets.drop(columns=['target_tracks'], inplace=True)
	
	return test_dataset, test_targets

#params= [(0,1,0), (1,1,0), (5,1,0), (5,0,0), (10,1,0), (10,0,0), (25,1,0), (25,1,1), (100,1,0), (100,1,1)]
params= [(5,1,0), (10,1,0), (25,1,0), (100,1,0)]

test_dataset, test_targets= get_test_data(params)

test_dataset.to_json(FILES_PATH+'test_dataset.json', orient='table')
test_targets.to_csv(FILES_PATH+'test_targets.csv', index=False, header=False)


