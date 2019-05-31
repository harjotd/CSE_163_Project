import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_id = "d5c7e6f8824c40f2ba7ac661b55fbeb3"
client_sec = "062661d5c3c6436997241777903492c1"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_sec)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

start = timeit.default_timer()


result = sp.track(track_id="0sSl9LFCzQAunHx9T1Un3O")
album_result = sp.album(album_id="3r5hf3Cj3EMh1C2saQ8jyt")
print(result['album']['id'])
print(album_result["popularity"])
