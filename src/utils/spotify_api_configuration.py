import spotipy
from spotipy.oauth2 import SpotifyOAuth

class MusicAPI:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-modify-playback-state user-read-playback-state",
            cache_path=".cache-spotify"  # guarda el token para no tener que loguearse siempre
        ))

    def _get_device_id(self):

        devices = self.sp.devices()

        if not devices["devices"]:
            print("No hay dispositivos disponibles.")
            return None
        
        return devices["devices"][0]["id"]

    def play_song(self, song_query):

        # Buscar canción
        results = self.sp.search(q=song_query, type="track", limit=1)
        items = results["tracks"]["items"]

        if not items:
            print("No se encontró la canción")
            return

        track = items[0]
        track_uri = track["uri"]
        song_name = track["name"]
        artist_name = track["artists"][0]["name"]

        # Obtener dispositivo
        device_id = self._get_device_id()
        if not device_id:
            return

        # Forzar reproducción nueva
        self.sp.start_playback(device_id=device_id, uris=[track_uri])

        # Activar loop en la pista
        self.sp.repeat(state="track", device_id=device_id)


    def pause(self):
        """Pausa la reproducción actual."""
        device_id = self._get_device_id()
        if device_id:
            self.sp.pause_playback(device_id=device_id)


    def resume(self):
        """Reanuda la reproducción."""
        device_id = self._get_device_id()
        if device_id:
            self.sp.start_playback(device_id=device_id)
