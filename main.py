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

# Google credentials
yt_credentials_path = 'path_to_your_google_credentials.json'
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

flow = InstalledAppFlow.from_client_secrets_file(yt_credentials_path, scopes)
credentials = flow.run_console()

youtube = build('youtube', 'v3', credentials=credentials)

# Fetch liked songs from Spotify
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

# Create YouTube playlist
def create_youtube_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    return response["id"]

# Search for song on YouTube
def search_youtube_video(youtube, query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=1,
        type="video"
    )
    response = request.execute()
    if response['items']:
        return response['items'][0]['id']['videoId']
    return None

# Add song to YouTube playlist
def add_video_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
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
    ).execute()

# Transfer songs from Spotify to YouTube
def transfer_songs_to_youtube(youtube, limit=50):
    liked_songs = fetch_spotify_liked_songs(limit)
    playlist_id = create_youtube_playlist(youtube, "My Spotify Liked Songs", "Songs I liked on Spotify transferred to YouTube")

    for song in liked_songs:
        track_name = song['track']['name']
        artist_name = song['track']['artists'][0]['name']
        search_query = f"{track_name} {artist_name}"
        video_id = search_youtube_video(youtube, search_query)
        if video_id:
            add_video_to_playlist(youtube, playlist_id, video_id)

# Transfer songs (specify the number of songs you want to transfer)
transfer_songs_to_youtube(youtube, limit=50)
