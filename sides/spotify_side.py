import os
import sys
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Utilizo UTF-8 para evitar problemas con los caracteres especiales 
sys.stdout.reconfigure(encoding='utf-8')


# Inicializa spotify
load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope='user-library-read'
))

# Func para traer las canciones likeadas (le podemos indicar un limite, o no. En caso de que no, traerá todo)
def fetch_spotify_liked_songs(limit=None):
    liked_songs, offset = [], 0
    while True:
        saved_tracks = sp.current_user_saved_tracks(limit=50 if limit is None else min(50, limit - len(liked_songs)), offset=offset)
        for track in saved_tracks['items']:
            song_name = track['track']['name']
            print(f"Saving song: {song_name}")

        liked_songs.extend(saved_tracks['items'])
        if len(saved_tracks['items']) < 50 or (limit is not None and len(liked_songs) >= limit):
            break
        offset += 50
    return liked_songs


# Func para traer las canciones de una playlist
def fetch_spotify_playlist_songs(playlist):
    if "spotify.com" in playlist:
        playlist_id = re.search(r'playlist/([a-zA-Z0-9]+)', playlist).group(1)
    else:
        playlist_id = playlist

    playlist_songs, offset = [], 0
    while True:
        playlist_tracks = sp.playlist_tracks(playlist_id, limit=50, offset=offset)
        playlist_songs.extend(playlist_tracks['items'])
        if len(playlist_tracks['items']) < 50:
            break
        offset += 50
    return playlist_songs
