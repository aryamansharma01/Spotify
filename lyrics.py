import types
import pandas as pd
import json
import requests
import sys
import spotipy
import spotipy.util as util
#from config.config import USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRETSPOTIPY_REDIRECT_URI
from bs4 import BeautifulSoup


# for acessing private playlists
scope = 'playlist-read-private'
username = '8eia8ggl4ipbhouhun62o9y8i'

token = util.prompt_for_user_token(username,
                                   scope, client_id='3cb41450f466404399f3e0de3e4c89f2',
                                   client_secret='51406619960a46c3a0fc8682e5152784',
                                   redirect_uri='http://localhost:8888/callback/')

# function for prinitng song name and lyrics


def show_lyrics(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
                                    track['name']))
        artist = track['artists'][0]['name']
        name = track['name']
        # formatting song url for
        song_url = '{}-{}-lyrics'.format(str(artist).strip().replace(' ', '-').replace('(', '').replace(')', ''),
                                         str(name).strip().replace(' ', '-').replace('(', '').replace(')', ''))
        print(song_url)

        request = requests.get("https://genius.com/{}".format(song_url))
        print(request.status_code)

        if request.status_code == 200:
            html_code = BeautifulSoup(request.text, features="html.parser")
            p = html_code.find("div", {"class": "lyrics"})
            if p is not None:
                lyrics = p.get_text()
                print(lyrics)
                print("-----------")

        else:
            print("Sorry, I can't find the actual song")


if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.playlist(playlist['id'],
                                  fields="tracks,next")
            tracks = results['tracks']

            show_lyrics(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)


else:
    print("Can't get token for", username)


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

#print(json.dumps(recentsongs, sort_keys=True, indent=2))
track = json.dumps(recentsongs, sort_keys=True, indent=2)
f = open('recentsongs.json',)
data = json.load(f)
f.close()
print(type(track))
# print(data)
# print(pd.read_json(tracks))
show_lyrics(recentsongs)
