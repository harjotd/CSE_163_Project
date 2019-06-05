import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config


def create_dataset():
    id = config.client_id
    sec = config.client_sec
    client_credentials_manager = SpotifyClientCredentials(client_id=id,
                                                          client_secret=sec)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
