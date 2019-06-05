import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config.py
import pandas as pd
# import cse163_utils  # noqa: F401
import pandas as pd


def parse():
    acoustics = pd.read_csv('CSE_163_Project\\Datasets\\acoustics.csv')
    billboard = pd.read_csv('CSE_163_Project\\Datasets\\billboard.csv')

    billboard = billboard[['date', 'album', 'rank', 'length', 'track_length']]
    billboard = billboard.rename(index=str, columns={"date": "list_date", "C": "c"})
    dataset = acoustics.merge(billboard, how='right', left_on='album',
                            right_on='album').dropna()
    unique_dataset = dataset['album'].unique().tolist()
    # Accessing Spotify API 
    id = config.client_id
    sec = config.client_sec
    client_credentials_manager = SpotifyClientCredentials(client_id=id,
                                                          client_secret=sec)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return len(unique_dataset)


print(parse())

def main():
    print(parse())


if __name__ == '__main__':
    main()
