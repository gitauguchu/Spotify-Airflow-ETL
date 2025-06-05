import pandas as pd
import requests
import datetime
import json
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri="https://localhost:8888/callback",
    scope="user-read-recently-played"
))

USER_ID = "b49da027e4e94e5fbe664e457970a590"
TOKEN = "402fb6855f644dba8a98dc69dc355d5e"

#Creating a function to be used in other python files
def return_dataframe():
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1) #Number of days you want the data for
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    #Download all the songs you've listened to in the last 24hrs 
    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}'.format(time=yesterday_unix_timestamp), headers=input_variables)
                     
    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    #Extracting only the relevant bits of data from the json object after checking whether the data exists
    if "items" in data:
        for song in data["items"]:
            song_names.append(song["track"]["name"])
            artist_names.append(song["track"]["album"]["artists"][0]["name"])
            played_at_list.append(song["played_at"])
            timestamps.append(song["played_at"][0:10])
    else:
        print("No 'items' found in the response. Full response:")
        print(json.dumps(data, indent=2))

    #Prepare a dictionary in order to turn it into a pandas dataframe below
    song_dict = {
        "song_name" : song_names,
        "artist_name" : artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    return song_df
