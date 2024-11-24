import sys
import sides.spotify_side as SS
import sides.youtube_side as YS

# Utilizo UTF-8 para evitar problemas con los caracteres especiales 
sys.stdout.reconfigure(encoding='utf-8')

## ======================= Main Script ========================
titulo_playlist = str(input('Ingrese titulo de la playlist: '))

operation = int(input('Deseas traer tu playlist de Me Gusta, o una playlist en especifico (1= Me Gusta, 0= Playlist especifica): '))

if operation == 1:
    limit_in = input('Quieres traer una cantidad especifica de canciones? O Todas? (en caso de ser todas, solo clickee enter): ')
    limit = int(limit_in) if limit_in else None
    songs = SS.fetch_spotify_liked_songs(limit)
elif operation == 0:
    link = str(input('Ingrese link (o ID) de la playlist: '))
    songs = SS.fetch_spotify_playlist_songs(link)
else:
    print('Valor invalido')
    
# Función principal para buscar canciones en YouTube desde Spotify
song_names = [f"{item['track']['name']} {item['track']['artists'][0]['name']}" for item in songs]
video_ids = YS.search_songs_on_yt(song_names)

if video_ids:
    # Creamos la playlist con el nombre elegido por el usuario
    playlist_id = YS.create_private_playlist(titulo_playlist, 'creado por SoundSwap')
    if playlist_id:
        # Añadimos las canciones a la playlist creada
        YS.add_videos_to_playlist(playlist_id, video_ids)
        print(f"Playlist creada exitosamente: https://www.youtube.com/playlist?list={playlist_id}")
else:
    print("No se encontraron videos para añadir a la playlist.")

