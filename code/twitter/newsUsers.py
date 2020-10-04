import csv
import os
import pandas as pd
import time
import tweepy

import login
auth = login.main()
api = tweepy.API(auth)
users = api.search_users(q='news Ohio', count = 20)

rootPath = '/home/jean/Documents/rescueDemocracy2020'
'''
linke to explanation of standard queries
https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/guides/standard-operators

'Pennsylvania' was found manually
'''
states = [
    'Minnesota',
    'Michigan',
    'Wisconsin',
    'Nevada',
    'Nebraska',
    'New_Hampshire',
    'Arizona',
    'North_Carolina',
    'Iowa',
    'Georgia',
    'Ohio',
    'Maine',
    'Florida',
    'Texas']

def channelUsers(station):
    output = []
    minimumFollowers = 1000

    users = api.search_users(q='news %s'%station, count = 20)
    for user in users:
        if user.followers_count >= minimumFollowers:
            output.append(user.id)
    return output

def stateUsers(state):
    # open .csv file of all stations
    stateFile = os.path.join(rootPath, 'data/twitterUsers', '%s.csv'%state)
    stations = pd.read_csv(stateFile, header = None)

    twitterFile = os.path.join(rootPath, 'data/twitterUsers', 'twitter%s.csv'%state)

    for i in stations.index:
        station = stations[0].iloc[i]
        print(i, station)
        time.sleep(15)
        newUsers = channelUsers(station)
        
        if i == 0:
            with open(twitterFile, 'w') as f:
                writer = csv.writer(f, delimiter=',')
                for user in newUsers:
                    writer.writerow([user])
        else:
            with open(twitterFile, 'a') as f:
                writer = csv.writer(f, delimiter=',')
                for user in newUsers:
                    writer.writerow([user])
    return

#get large array of all stations together


# save the results to .csv file
def saveNewUsers(newList):
    fileName = 'allNewsTwitter.csv'
    fullPath = os.path.join(rootPath, 'data', fileName)

    df = pd.read_csv(fullPath, header=None)

    newList = [user.name for user in newList]
    output = pd.Series(df.values + newList)

    ouput.to_csv(fullPath, index=False)

def cleanString(station):
    location = station.find('-')
    dash = len(station) if location == -1 else location

    location = station.find('(')
    parenthesis = len(station) if location == -1 else location
    return station[:min(dash, parenthesis)].strip()

def saveStations(state):
    fullFile = os.path.join(rootPath, 'data/twitterUsers', 'wiki%s.csv'%state)
    df = pd.read_csv(fullFile)
    stationColumn = 'Callsign' if 'Callsign' in df.columns else 'Call Letters'
    df['output'] = df[stationColumn].apply(lambda station: cleanString(station))

    saveFile = os.path.join(rootPath, 'data/twitterUsers', '%s.csv'%state)
    df['output'].to_csv(saveFile, index = False, header = False)
    return

def main():
    for state in states:
        print(state)
        stateUsers(state)

'''
parse the tables from wikipedia using
Wiki Table to CSV online converter
wikitable2csv.ggor.de
https://en.wikipedia.org/wiki/List_of_television_stations_in_Pennsylvania
https://en.wikipedia.org/wiki/List_of_television_stations_in_Minnesota
https://en.wikipedia.org/wiki/List_of_television_stations_in_Michigan
https://en.wikipedia.org/wiki/List_of_television_stations_in_Wisconsin
https://en.wikipedia.org/wiki/List_of_television_stations_in_Nevada
https://en.wikipedia.org/wiki/List_of_television_stations_in_Nebraska
https://en.wikipedia.org/wiki/List_of_television_stations_in_New_Hampshire
https://en.wikipedia.org/wiki/List_of_television_stations_in_Arizona
https://en.wikipedia.org/wiki/List_of_television_stations_in_North_Carolina
https://en.wikipedia.org/wiki/List_of_television_stations_in_Iowa
https://en.wikipedia.org/wiki/List_of_television_stations_in_Georgia_(U.S._state)
https://en.wikipedia.org/wiki/List_of_television_stations_in_Ohio
https://en.wikipedia.org/wiki/List_of_television_stations_in_Maine
https://en.wikipedia.org/wiki/List_of_television_stations_in_Florida
https://en.wikipedia.org/wiki/List_of_television_stations_in_Texas
'''