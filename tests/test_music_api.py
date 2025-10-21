import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.spotify_api_configuration import MusicAPI

api = MusicAPI(
    client_id="f4c8500d173141c4b597107c86b357e2",
    client_secret="2a325628d37e4cdb9c6245195d116ccc",
    redirect_uri="http://127.0.0.1:8888/callback"
)

api.play_song("b2b")

#Se prueba que puede cambiar la canción en cualquier momento:
time.sleep(15)
api.play_song("motherlode")

