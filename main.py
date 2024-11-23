import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


# Autenticación con OAuth 2.0 (YT)
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = InstalledAppFlow.from_client_secrets_file(r"info sensible\youtube-credentials.json", scopes)
credentials = flow.run_local_server(port=8080)

# Construir el servicio de YouTube
youtube = build("youtube", "v3", credentials=credentials)

load_dotenv()

# Utilizo UTF-8 para evitar problemas con los caracteres especiales 
sys.stdout.reconfigure(encoding='utf-8')

# Inicializa spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope='user-library-read'
))

# Func para traer las canciones likeadas (indicando un limite)
def fetch_spotify_liked_songs(limit):
    liked_songs, offset = [], 0
    while len(liked_songs) < limit:
        saved_tracks = sp.current_user_saved_tracks(limit=min(50, limit - len(liked_songs)), offset=offset)
        liked_songs.extend(saved_tracks['items'])
        if len(saved_tracks['items']) < 50:
            break
        offset += 50
    return liked_songs

# Crear la lista de reproducción privada
def create_private_playlist(titulo, descripcion):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": titulo,
                "description": descripcion
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    print(f"Lista de reproducción creada: {response['snippet']['title']}")


# liked_songs = fetch_spotify_liked_songs(50)
# for song in liked_songs:
#     track_name = song['track']['name']
#     artist_name = song['track']['artists'][0]['name']  # Solo traer el primer artista
#     print(f"{track_name} - {artist_name}")



