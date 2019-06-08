import pandas as pd
import spotipy as spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as mplot
import seaborn as sns
import time
import config
from datetime import datetime
import calendar
import numpy as np
sns.set()


ACOUSTICS = 'acoustics.csv'
BILLBOARD = 'billboard.csv'


def parse(file_1, file_2):
    '''Takes in a two CSV files as a parameter, acoustics first, then
    billboard. The function will return a new dataset with the two passed
    in datasets merged, and it will also create a column that contains the
    popularity of the album through accessing the Spotfiy API.'''
    acoustics = pd.read_csv(file_1)
    billboard = pd.read_csv(file_2)

    billboard = billboard[['date', 'album', 'rank', 'length', 'track_length']]
    billboard = billboard.rename(index=str, columns={"date": "list_date"})
    dataset = acoustics.merge(billboard, how='right', left_on='album',
                              right_on='album').dropna()
    dataset = dataset[['date', 'album', 'rank', 'length', 'list_date',
                       'danceability', 'album_id', 'artist']]
    dataset = dataset[dataset['album'] != "Greatest Hits"]

    # spotfy api object
    id = config.client_id
    sec = config.client_sec
    client_credentials_manager = SpotifyClientCredentials(client_id=id,
                                                          client_secret=sec)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    alids = dataset['album_id'].unique()
    ddata = dict()
    for i in range(0, len(alids)):
        ddata[alids[i]] = sp.album(album_id=alids[i])['popularity']
        if i % 1000 == 0:
            print("RUNNING")
            time.sleep(10)
    df1 = pd.DataFrame(list(ddata.items()), columns=['album_id', 'popularity'])
    dataset = dataset.merge(df1, left_on='album_id', right_on='album_id',
                            how='inner')
    dataset.to_csv('mainset.csv')
    return dataset


def problem1(data):
    """plot danceability(from dataset) and popularity(spotify api)"""
    data1 = data.groupby('album')['danceability'].mean()
    newdata = pd.DataFrame({'album': data1.index,
                            'album_danceability': data1.values})
    # i is the dataset used for this function
    i = data.merge(newdata, left_on='album', right_on="album", how='right')
    # i is now a table of album danceability values and popularity, with each
    # row representing a unique album
    i = i[['album', 'album_danceability', 'popularity']].drop_duplicates()
    sns.regplot(data=i, x='album_danceability', y='popularity')
    mplot.show()
    correlation = np.corrcoef(i['album_danceability'], i['popularity'])
    # [0][1] is a good value
    print("Correlation Coefficient:", correlation[0][1])


def popularity(data):
    '''Takes in data as a parameter. This will create 4 charts of popularity,
    one on day of the week (Monday-Sunday), one on day of the month (1-31),
    one on month itself, and the last one on season. Each will represent the
    amount of top 10 albums that released within those time periods.'''
    popular = data[data['rank'] <= 10]
    popular = data[['album', 'date']]
    popular = popular.drop_duplicates(subset=['album', 'date'])
    month = pd.to_datetime(popular['date']).dt.month
    day = pd.to_datetime(popular['date']).dt.day
    year = pd.to_datetime(popular['date']).dt.year
    popular['month'], popular['day'], popular['year'] = month, day, year

    # Day of Week
    day_name = popular
    day_list, month_list = day.tolist(), month.to_list()
    year_list = year.to_list()
    day_of_week = list()
    for counter in range(0, len(day_name)):
        date = datetime(year_list[counter], month_list[counter],
                        day_list[counter])
        day_of_week.append(calendar.day_name[date.weekday()])
    day_name['Day'] = day_of_week
    week_day = day_name['Day'].value_counts()
    week_day = pd.DataFrame({"Day": week_day.index,
                             "# Of Top 10 Releases": week_day.values})
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                 "Saturday", "Sunday"]
    ax = week_day.set_index("Day").loc[day_order].plot(kind="bar")
    ax.set_ylabel("Counts")
    mplot.savefig("Most Popular Day(M-S).png")

    # Numerical Day
    days = popular['day'].value_counts().sort_index()
    days = pd.DataFrame({"Day": days.index,
                         '# of Top 10 Releases': days.values})
    days.plot(x="Day", kind='bar')
    mplot.savefig('Most Popular Day(1-31).png')

    # Month
    values = popular['month'].value_counts().sort_index()
    if len(values.index) == 12:
        values.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                        'Sep', 'Oct', 'Nov', 'Dec']
    months = pd.DataFrame({'Month': values.index, 'Count': values.values})
    months.plot(x="Month", kind='bar')
    mplot.savefig("Most Popular Month.png")

    # Seasons
    month_to_season = dict({1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring",
                            5: "Spring", 6: "Summer", 7: "Summer", 8: "Summer",
                            9: "Fall", 10: "Fall", 11: "Fall", 12: "Winter"})
    season_df = popular
    season_df = season_df.rename(index=str, columns={"month": "season"})
    season_df['season'].replace(month_to_season, inplace=True)
    season_df = season_df['season'].value_counts()
    season_df = pd.DataFrame({'Season': season_df.index,
                              'Count': season_df.values})
    season_df.plot(x='Season', kind='bar')
    mplot.savefig("Most Popular Season.png")


def unique_artists(data):
    '''Takes in the merged dataset as a parameter. It will save a plot
    that plots out how many unique artists appeared per year in the Billboard
    Top 200.'''
    year = pd.to_datetime(data['date']).dt.year
    data['year'] = year
    data = data[['artist', 'year']]
    per_year = data.drop_duplicates(subset=['artist', 'year'])
    per_year = per_year.groupby('year')['artist'].count()
    per_year = pd.DataFrame({'Year': per_year.index, 'Count': per_year.values})
    per_year = per_year[per_year['Year'] != 2019]
    plot = sns.lineplot(x='Year', y='Count', data=per_year)
    plot.figure.savefig("Unique Artists.png")


def top_10(data):
    '''Takes in the merged dataset as a parameter. It will save a plot that
    contains a graph on the top 10 albums that appeared in the Billboard
    Top 10 the most amount of times.'''
    top_10_rank = data[data['rank'] <= 10]
    top_10_rank = top_10_rank[['album', 'rank', 'list_date']]
    top_10_rank = top_10_rank.drop_duplicates(subset=['album', 'rank',
                                                      'list_date'])
    highest_ranked = top_10_rank['album'].value_counts()
    highest_ranked = highest_ranked.sort_values(ascending=False)
    highest_ranked = pd.DataFrame({'Album': highest_ranked.index,
                                  '# of Appearances': highest_ranked.values})
    highest_ranked = highest_ranked.head(10)
    ax = sns.barplot(x='Album', y='# of Appearances', data=highest_ranked)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    mplot.tight_layout()
    mplot.savefig("Most Frequent Top 10 Albums.png")


def main():
    data = parse(ACOUSTICS, BILLBOARD)
    problem1(data)
    popularity(data)
    unique_artists(data)
    top_10(data)


if __name__ == '__main__':
    main()
