import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# ##### pasted in #########

# import cse163_utils  # noqa: F401
import pandas as pd

ACOUSTICS = 'project/acoustics.csv'  # why does vscode sometimes get the wrong
BILLBOARD = 'project/billboard.csv'  # file path?


def parse(file_1, file_2):
    acoustics = pd.read_csv(file_1)
    billboard = pd.read_csv(file_2)

    billboard = billboard[['date', 'album', 'rank', 'length', 'track_length']]
    billboard = billboard.rename(index=str, columns={"date": "list_date", "C": "c"})
    dataset = acoustics.merge(billboard, how='right', left_on='album',
                            right_on='album').dropna()
    return dataset.head(50)


def main():
    print(parse(ACOUSTICS, BILLBOARD))


if __name__ == '__main__':
    main()
