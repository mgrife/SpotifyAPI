import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import base64
import json
from secrets import *
import csv
import sqlite3

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
    with open("Spotify.csv", "w", newline ='') as f:
        writer = csv.writer(f)
        writer.writerow(["Value", "Artist Name", "Song Name", "Popularity Score"])
        count = 1
        for id in idlist:
            params = {'id': id}
            response = requests.get(base_url.format(id = id), headers=headers, params=params).json()
            writer.writerow([count, response['artists'][0]['name'], response['name'], response['popularity']])
            ##f.writerow(str(count) + "," + response['artists'][0]['name'] + "," +  response['name'] +  "," +str(response['popularity']) + "\n")
            count += 1
            # print(response['artists'][0]['name'])
            # print(response['popularity'])
            # print(response['name'])

early = get_track_ids(read_in_top_songs())
#get_popularity_score(early)

def create_Spotify_db():

    # Connect to a new database (creates a new file if it doesn't exist)
        conn = sqlite3.connect('Spotify_Table.db')

        # Create a new table to hold the CSV data
        conn.execute('''CREATE TABLE IF NOT EXISTS Spotify_Table
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Value INT,
                        Artist_Name TEXT,
                        Song_Name TEXT,
                        Popularity INT);''')

        # Open the CSV file and read its contents
        with open('Spotify.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Skip the header row
            next(csv_reader)

            # Insert each row of the CSV data into the table
            for row in csv_reader:
                #print(row)
                conn.execute("INSERT INTO Spotify_Table (Value, Artist_Name, Song_Name, Popularity) VALUES (?, ?, ?, ?)", row)

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

#create_Spotify_db()

def create_Youtube_db():

    # Connect to a new database (creates a new file if it doesn't exist)
        conn = sqlite3.connect('Spotify_Table.db')

        # Create a new table to hold the CSV data
        conn.execute('''CREATE TABLE IF NOT EXISTS Youtube_Table
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Value INT,
                        Music_Video TEXT,
                        View_Count INT,
                        Like_Count INT,
                        Dislike_Count INT,
                        Comment_Count INT);''')

        # Open the CSV file and read its contents
        with open('youtube.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Skip the header row
            next(csv_reader)

            # Insert each row of the CSV data into the table
            for row in csv_reader:
                print(row)
                conn.execute("INSERT INTO Youtube_Table (Value, Music_Video, View_Count, Like_Count, Dislike_Count, Comment_Count) VALUES (?, ?, ?, ?, ?, ?)", row)

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()
 
create_Youtube_db()