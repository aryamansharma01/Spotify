import types
import pandas as pd
import json
import requests
import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
# from config.config import USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRETSPOTIPY_REDIRECT_URI
from bs4 import BeautifulSoup


# for acessing private playlists
scope = 'playlist-read-private'
username = '8eia8ggl4ipbhouhun62o9y8i'
client_id = '3cb41450f466404399f3e0de3e4c89f2'
client_secret = '51406619960a46c3a0fc8682e5152784'
redirect_uri = 'http://localhost:8888/callback/'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
token = util.prompt_for_user_token(username, scope, client_id, client_secret,
                                   redirect_uri)


def current_user_recently_played(self, limit=50):
    return self._get('me/player/recently-played', limit=limit)


token = util.prompt_for_user_token(
    username='8eia8ggl4ipbhouhun62o9y8i',
    scope="user-read-recently-played user-read-private user-top-read user-read-currently-playing",
    client_id='3cb41450f466404399f3e0de3e4c89f2',
    client_secret='51406619960a46c3a0fc8682e5152784',
    redirect_uri='http://localhost:8888/callback/')

spotify = spotipy.Spotify(auth=token)
spotify.current_user_recently_played = types.MethodType(current_user_recently_played, spotify)

recentsongs = spotify.current_user_recently_played(limit=50)
out_file = open("recentsongs.json", "w")
out_file.write(json.dumps(recentsongs, sort_keys=True, indent=2))
out_file.close()

# print(json.dumps(recentsongs, sort_keys=True, indent=2))
# track = json.dumps(recentsongs, sort_keys=True, indent=2)
f = open('recentsongs.json',)
data = json.load(f)
f.close()
track_id = []
track_name = []
for i in recentsongs['items']:
    track_id.append(i['track']['id'])
    track_name.append(i['track']['name'])

features = []
tracks = {}
for track in track_id:
    features.append(sp.audio_features(track))
for i in range(0, 49):
    tracks[i+1] = {}
for i in range(0, 49):
    tracks[i+1]['number'] = i+1
    tracks[i+1]['name'] = track_name[i]
    tracks[i+1]['id'] = track_id[i]
    tracks[i+1]['acousticness'] = features[i][0]['acousticness']
    tracks[i+1]['danceability'] = features[i][0]['danceability']
    tracks[i+1]['energy'] = features[i][0]['energy']
    tracks[i+1]['instrumentalness'] = features[i][0]['instrumentalness']
    tracks[i+1]['liveness'] = features[i][0]['liveness']
    tracks[i+1]['loudness'] = features[i][0]['loudness']
    tracks[i+1]['speechiness'] = features[i][0]['speechiness']
    tracks[i+1]['tempo'] = features[i][0]['tempo']
    tracks[i+1]['valence'] = features[i][0]['valence']
    pop = sp.track(track_id[i])
    tracks[i+1]['popularity'] = pop['popularity']
feature = ['number', 'name', 'id', 'acousticness', 'danceability', 'energy',
           'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence',
           'popularity']
dic_df = {}
for x in feature:
    dic_df[x] = []
for j in range(1, 50):
    for x in feature:
        dic_df[x].extend([tracks[j][x]])
dataframe = pd.DataFrame.from_dict(dic_df)
print(dataframe)
