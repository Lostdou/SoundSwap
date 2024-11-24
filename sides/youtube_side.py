import sys
import logging
from pytube import Search
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Configurar el nivel de logging para PyTube
logging.getLogger("pytube").setLevel(logging.ERROR)
# Utilizo UTF-8 para evitar problemas con los caracteres especiales 
sys.stdout.reconfigure(encoding='utf-8')


# Autenticación con OAuth 2.0 (YT)
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = InstalledAppFlow.from_client_secrets_file(r"info sensible\youtube-credentials.json", scopes)
credentials = flow.run_local_server(port=8080)

# Construir el servicio de YouTube
youtube = build("youtube", "v3", credentials=credentials)

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
    playlist_id = response.get('id')  # Extract the playlist ID
    return playlist_id

# Añadir las canciones a una playlist
def add_videos_to_playlist(playlist_id, video_ids):
    for video_id in video_ids:
        try:
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id 
                        }
                    }
                }
            )
            response = request.execute()
            print(f"Video añadido: {video_id}")
        except Exception as e:
            print(f"Error añadiendo video {video_id}: {str(e)}")

# Buscamos las canciones con PyTube para ahorrar creditos
def search_songs_on_yt(songs):
    video_ids = []
    for song in songs:
        try:
            s = Search(song)
            result = s.results
            if result:
                print('Video encontrado: ',result[0].video_id)
                video_ids.append(result[0].video_id)
        except Exception as e:
            print(f"Error buscando {song}: {str(e)}")
    return video_ids
