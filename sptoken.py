from flask import Flask, redirect
import requests
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

app = Flask(__name__)
app.secret_key = ""

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

REDIRECT_URI = "https://localhost:8888/callback"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Log in to Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-recently-played'

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)