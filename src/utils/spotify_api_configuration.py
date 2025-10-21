import spotipy
from spotipy.oauth2 import SpotifyOAuth

class MusicAPI:

    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-modify-playback-state user-read-playback-state"
        ))


    def play_song(self, song_query):
    
        res = self.sp.search(q=song_query, type="track", limit=1)
        items = res.get("tracks", {}).get("items", [])

        if not items:
            print("No encontré la canción.")
            return
        
        track_uri = items[0]["uri"]

        devs = self.sp.devices().get("devices", [])
        if not devs:
            print("No hay dispositivos disponibles.")
            return
        
        device_id = devs[0]["id"]

        self.sp.start_playback(device_id=device_id, uris=[track_uri])
        self.sp.repeat(state="track", device_id=device_id)

           
