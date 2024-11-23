import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Spotify credentials
sp_client_id = os.getenv('SPOTIFY_CLIENT_ID')
sp_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
sp_redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=sp_client_id,
    client_secret=sp_client_secret,
    redirect_uri=sp_redirect_uri,
    scope='user-library-read'
))

# Request de las canciones likeadas
def fetch_spotify_liked_songs(limit):
    all_liked_songs = []
    offset = 0
    while len(all_liked_songs) < limit:
        saved_songs = sp.current_user_saved_tracks(limit=min(50, limit - len(all_liked_songs)), offset=offset)
        all_liked_songs.extend(saved_songs['items'])
        if len(saved_songs['items']) < 50:
            break
        offset += 50
    return all_liked_songs

# Request de las canciones de una playlist especifica
def fetch_spotify_playlist_songs(playlist_id, limit):
    all_playlist_songs = []
    offset = 0
    while len(all_playlist_songs) < limit:
        playlist_songs = sp.playlist_tracks(playlist_id, limit=min(50, limit - len(all_playlist_songs)), offset=offset)
        all_playlist_songs.extend(playlist_songs['items'])
        if len(playlist_songs['items']) < 50:
            break
        offset += 50
    return all_playlist_songs
