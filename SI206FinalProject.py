import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import base64
import json
from secrets import *
import csv


import os


# Step 1 - Authorization 

def CreateToken():
        
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    

    data ={}


    # Encode as Base64
    clientId = "19010435a701468aaaac1fc85ab56058"
    clientSecret = "86d0ad27dfb14dfbbea6698626bff9d8"

    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')


    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']
    
    return token

# def get_top_150():
#     base_url = "https://api.spotify.com/v1/me/top/{type}"
#     token = CreateToken()
#     headers = {'Authorization': 'Bearer ' + token}
#     # params = {'type': "tracks", 'time_range': "medium_term", "limit":}
#     # response = requests.get(base_url.format(id = id), headers=headers, params=params).json()
#     response = requests.get("https://api.spotify.com/v1/charts/top", headers=headers, params={"limit": 150})
    
# # Get the names of the top 150 tracks
#     top_tracks = []
#     if response.status_code == 200:
#         data = json.loads(response.text)
#         for track in data["tracks"]:
#             print(data["tracks"])
#             print(track["name"])
#             top_tracks.append(track["name"])

#     print(top_tracks)

def read_in_top_songs():
    top_song_names = []
    with open("desktop/charts.csv", "r") as f:
        
        next(f)
        for line in f:
            
            top_song_names.append(line.split(",")[2])

    return top_song_names




def get_track_ids(song_names):
    track_ids = []
    base_url = 'https://api.spotify.com/v1/search'
    token = CreateToken()
    headers = {'Authorization': 'Bearer ' + token}
               
    for song in song_names:
        # search for the song on Spotify
        params = {'q': song, 'type': 'track'}
        response = requests.get(base_url, headers=headers, params=params).json()
        track_id = response['tracks']['items'][0]['id']
        track_ids.append(track_id)

    return track_ids

listofsong = ["Unwritten", "You Belong With Me", "Death by a Thousand Cuts", "All too well", "Dress", "Midnight Rain"]
#print(get_track_ids(read_in_top_songs()))

def get_popularity_score(idlist):
    base_url = "https://api.spotify.com/v1/tracks/{id}"
    token = CreateToken()
    headers = {'Authorization': 'Bearer ' + token}
    with open("Spotify.csv", "w") as f:

        f.write("Artist Name, Song Name, Popularity Score\n")

        for id in idlist:
            params = {'id': id}
            response = requests.get(base_url.format(id = id), headers=headers, params=params).json()
            f.write(response['artists'][0]['name'] + "," + response['name'] + "," +str(response['popularity']) + "\n")
            # print(response['artists'][0]['name'])
            # print(response['popularity'])
            # print(response['name'])

early = get_track_ids(read_in_top_songs())
get_popularity_score(early)

