import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import timeit

client_id = "d5c7e6f8824c40f2ba7ac661b55fbeb3"
client_sec = "062661d5c3c6436997241777903492c1"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_sec)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

start = timeit.default_timer()

# create empty lists where the results are going to be stored
artist_name = []
track_name = []
popularity = []
track_id = []

for i in range(0,100,50):
    track_results = sp.search(q='year:2018', type='track', limit=50,offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
      
print(popularity)
stop = timeit.default_timer()
print ('Time to run this code (in seconds):', stop - start)


result = sp.track(track_id="0sSl9LFCzQAunHx9T1Un3O")
album_result = sp.album(album_id="3r5hf3Cj3EMh1C2saQ8jyt")
print(result['album']['id'])
print(album_result["popularity"])
sp.

dataset[].head(50)