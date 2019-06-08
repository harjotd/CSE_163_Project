import final_project as fp
import pandas as pd


def problem1_test(data):
    data_up = data.head(5)
    rigged_danceability = [1, 1, 1, 1, 1]
    rigged_popularity = [4, 2, 4, 5, 2]
    data_up['danceability'] = rigged_danceability
    data_up['popularity'] = rigged_popularity
    print("Rigged Correlation Coefficient:", fp.problem1(data_up))


def popularity_test(data):
    '''Takes in a parameter of a smaller testset, size of 10. It will print
    out the results of the popularity method, tested on a smaller sample
    size.'''
    data_up = data
    new_dates = ['2019-02-22', '2019-02-22', '2019-02-12', '2015-02-22',
                 '2014-02-22', '2015-02-22', '1999-02-22', '2009-02-12',
                 '2011-02-22', '2013-02-22']
    data_up['date'] = new_dates
    fp.popularity(data_up)


def unique_artists_test(data):
    '''Takes in a smaller dataset as a parameter. It tests the unique_artist
    function, and plots out the resulting amount of unique artists.'''
    data_unique = data
    artists = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'H', 'I']
    year = ['2000-02-22', '2000-02-22', '2000-02-22', '2001-02-22',
            '2001-02-22', '2001-02-22', '2002-02-22', '2003-02-22',
            '2003-02-22', '2003-02-22']
    list_date = ['2000-02-24', '2000-02-23', '2000-02-21', '2001-02-20',
                 '2001-02-12', '2001-02-26', '2002-02-27', '2003-02-11',
                 '2003-02-13', '2003-02-15']
    data_unique['list_date'] = list_date
    data_unique['artist'] = artists
    data_unique['date'] = year
    fp.unique_artists(data_unique)


def top10_test(data):
    '''Takes a smaller dataset as a parameter, and plots out the top 10
    most freqeunt albums listed in the top 10, based off of a smaller
    sample size.'''
    data_top10 = data
    album = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'D', 'F', 'F']
    rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data_top10['album'] = album
    data_top10['rank'] = rank
    fp.top_10(data_top10)


def main():
    data = pd.read_csv("testset.csv")
    problem1_test(data)
    popularity_test(data)
    unique_artists_test(data)
    top10_test(data)


if __name__ == "__main__":
    main()
