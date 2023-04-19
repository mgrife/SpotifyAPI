import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import base64
import json
from secrets import *
import csv

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

listofsong = ["Unwritten"]
#print(get_track_ids(listofsong))

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
            print(response['artists'][0]['name'])
            print(response['popularity'])
            print(response['name'])



ids = ['3U5JVgI2x4rDyHGObzJfNf']
get_popularity_score(ids)




        # get the track ID from the first result (if any)
        # if 'tracks' in response and 'items' in response['tracks'] and len(response['tracks']['items']) > 0:
        #     track_id = response['tracks']['items'][0]['id']
        #     track_ids.append(track_id)


# def gettoken():
#     curl -X POST "https://accounts.spotify.com/api/token" 
#      -H "Content-Type: application/x-www-form-urlencoded" 
#      -d "grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret"


#print(CreateToken())
# Step 2 - Use Access Token to call playlist endpoint

# playlistId = "6dkC25oqwGAIkPneVONR0K"
# playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"
# headers = {
#     "Authorization": "Bearer " + token
# }

# res = requests.get(url=playlistUrl, headers=headers)

# print(token)
#print(json.dumps(res.json(), indent=2))
