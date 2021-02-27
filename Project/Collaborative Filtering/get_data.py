import timeit
import json
import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
from parameters import *


#proxies= {
#    "http":"http://ee1170463:kJLVKWu3@10.10.78.22:3128/",
#    "https":"http://ee1170463:kJLVKWu3@10.10.78.22:3128/"
#}

playlist_cols= ["name", "collaborative", "pid", "modified_at", "num_albums",
                   "num_tracks", "num_followers", "num_edits", "duration_ms", 
                    "num_artists", "tracks"]
tracks_cols= ["artist_name", "track_uri", "artist_uri", "track_name", "album_uri",
                 "duration_ms", "album_name", "tid"]
tid= 0

def append_track(track, track_list, tr_uri2id, tracks_dict):
    global tid
    track_uri= track['track_uri']
    if track_uri not in tr_uri2id:
        for key in tracks_cols[:-1]:
            tracks_dict[key].append(track[key])
        tracks_dict["tid"].append(tid)
        tr_uri2id[track_uri]= tid   
        tid+=1
    track_list.append(tr_uri2id[track_uri])
    
def read_data():
    playlist_dict= {}
    for key in playlist_cols:
        playlist_dict[key]= []
    
    tracks_dict= {}
    for key in tracks_cols:
        tracks_dict[key]= []

    tr_uri2id= {}

    file_names= os.listdir(DATA_PATH)
    for file_name in file_names:
        print(file_name)
        json_data= json.load(open(DATA_PATH+file_name))
        data= json_data['playlists']
    
        for playlist in data:
            tracks= playlist["tracks"]
            for key in playlist_cols[:-1]:
                playlist_dict[key].append(playlist[key])
            
            tracks_list= []
            for track in tracks:
                append_track(track, tracks_list, tr_uri2id, tracks_dict)
            playlist_dict["tracks"].append(tracks_list)
            
    playlist_df= pd.DataFrame(playlist_dict).set_index('pid').sort_index()
    tracks_df= pd.DataFrame(tracks_dict).set_index('tid').sort_index()

    return playlist_df, tracks_df, tr_uri2id

def augment_data(tracks_df):
    scc= SpotifyClientCredentials(client_id= CLIENT_ID, client_secret= CLIENT_SECRET, proxies=proxies)
    sp= spotipy.Spotify(client_credentials_manager= scc, proxies=proxies)

    additional_feats= ['danceability', 'energy', 'speechiness', 'mode', 'acousticness', 
                       'instrumentalness', 'liveness', 'valence', 'tempo']

    tracks_df= pd.concat([tracks_df, pd.DataFrame(columns= additional_feats)])

    for idx in range(0, len(tracks_df), 100):
        print(idx, end="\r")
        up= idx+100 if idx+100<len(tracks_df) else len(tracks_df)
        track_features= sp.audio_features(tracks_df["track_uri"][idx:up].tolist())
        for feat in additional_feats:
            tracks_df.loc[idx:up, additional_feats]= pd.DataFrame(track_features, columns= additional_feats)

    return tracks_df

playlist_df, tracks_df, tr_uri2id= read_data()
#tracks_df= augment_data(tracks_df)

with open(FILES_PATH+"uri2id.pkl",'wb') as f:
    pickle.dump(tr_uri2id, f)
tracks_df.to_csv(FILES_PATH+'tracks.csv')
playlist_df.to_csv(FILES_PATH+'playlists.csv')
