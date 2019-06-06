

# import cse163_utils  # noqa: F401
import pandas as pd
import spotipy as spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as mplot
import seaborn as sns
import time
import config

ACOUSTICS = 'project/acoustics.csv'  # why does vscode sometimes get the wrong
BILLBOARD = 'project/billboard.csv'  # file path?


def parse(file_1, file_2):
    acoustics = pd.read_csv(file_1)
    billboard = pd.read_csv(file_2)

    billboard = billboard[['date', 'album', 'rank', 'length', 'track_length']]
    billboard = billboard.rename(index=str, columns={"date": "list_date", "C": "c"})
    dataset = acoustics.merge(billboard, how='right', left_on='album',
                              right_on='album').dropna()
    id = config.client_id
    sec = config.client_sec
    client_credentials_manager = SpotifyClientCredentials(client_id=id,
                                                          client_secret=sec)
    # spotfy api object
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    alids = dataset['album_id'].unique()
    ddata = dict()
    print(alids)
    print(len(alids))
    for i in range(0, len(alids)):
        ddata[alids[i]] = sp.album(album_id=alids[i])['popularity']
        if i % 1000 == 0:
            time.sleep(10)
    print(ddata)
    df1 = pd.DataFrame(list(ddata.items()), columns=['album_id', 'popularity'])
    print(df1)
    dataset = dataset.merge(df1, left_on='album_id', right_on='album_id', how='inner')
    print('here')
    # print(dataset['popularity'])
    dataset.to_csv('testset.csv')
    # need to pull: album popularity from song ID, genre, popularity
    return None
    # return dataset.head(50)


def problem1(data):
    """plot danceability(from datatable) and popularity(spotify api)"""
    sns.regplot(x='danceability', y='popularity', data=data)
    mplot.show()
    return None


def problem2(data):
    """  """
    data = data[data['popularity'] >= 0.7]
    """ 4 axes for season, month, week, date """
    fig, [[ax1, ax2], [ax3, ax4]] = mplot.subplots(2, figsize=(20, 10),
                                                   ncols=2)
    """ groupby time-date value with respect to: day of month"""
    """add day of week column, write code from time-date data"""
    """add season column """
    """add month column"""


def problem3(data):
    """take genre column,"""


def test():
    id = config.client_id
    sec = config.client_sec
    client_credentials_manager = SpotifyClientCredentials(client_id=id,
                                                          client_secret=sec)
    # spotfy api object
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    result = sp.track(track_id="0sSl9LFCzQAunHx9T1Un3O")
    album_result = sp.album(album_id="3r5hf3Cj3EMh1C2saQ8jyt")
    print(result['album']['name'])
    print(album_result)


def main():
    print(parse(ACOUSTICS, BILLBOARD))
    # test()
    # print(parse1())


if __name__ == '__main__':
    main()
