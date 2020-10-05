import csv
import os
import pandas as pd

import login

rootPath = '/home/jean/Documents/rescueDemocracy2020'

badWords = [
    'savethechildren',
    'savethechildrenworldwide',
    'childtrafficking',
    'lolitaexpress',
    'wwg1gwaw',
    'saveourchildren',
    '10daysofdarkness',
    'wwg1gwa ',
    'qanon2020',
    'trusttheplan',
    'followthewhiterabbit',
    'greatawakeningworldwide',
    'redoctober',
    'pedophile',
    'pedophilia',
    'child predator']

# create array consisting of all target twitter accounts
def accountNames():
    fileName = os.path.join(rootPath, 'data', 'twitter.csv')
    with open(fileName, newline='') as f:
        content = f.readlines()
    return [name.rstrip('\n') for name in content]

#create folder structure to store data, 
#if not already available
def makeFolders(names):
    for name in names:
        newFolder = os.path.join(rootPath, 'data', name)
        # check if folder doesn't yet exist
        if not os.path.exists(newFolder):
            # create new subfolder
            os.mkdir(newFolder)

# Get a list of recent tweets from news site
# check responses for misinformation

'''
get replies to a particular person, regardless of the story or original post
'''
def getAllReplies(targetId):
    user = api.get_user(targetId)
    replies=[]
    for tweet in tweepy.Cursor(api.search,q='@'+user.screen_name, result_type='recent'):
        if any([el in tweet.text.lower() for el in badWords]):
            replies.append(tweet.id, tweet.text)
    return replies

# get replies to tweets
def getReplies(tweet_id, target):
    replies=[]
    for tweet in tweepy.Cursor(api.search,q='to:'+target, result_type='recent', timeout=999999).items(10):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                replies.append(tweet)
    return replies
########################################################################
# Only iterate through the first few items

def statusFile(target, numberPosts):
    tweet_ids, tweet_texts = [], []
    for status in tweepy.Cursor(api.user_timeline, id=target).items(numberPosts):
        tweet_texts.append(status.text)
        tweet_ids.append(status.id)

    # save the tweet IDs along with the text in a .csv file
    fileName = os.path.join(rootPath, 'data', target, 'status.csv')
    statusTweets = pd.DataFrame(columns = ['id', 'text'])
    statusTweets['id'] = tweet_ids
    statusTweets['text'] = tweet_texts
    statusTweets.to_csv(fileName, index = False)        

    return tweet_texts, tweet_ids

def statusFileToday(target):
    tweet_ids, tweet_texts = [], []
    # Get date today format "2018-11-16"
    now = datetime.datetime.now()
    today = str(datetime.date(now.year, now.month, now.day))

    for status in tweepy.Cursor(api.user_timeline, id=target).items(20):
        tweet_texts.append(status.text)
        tweet_ids.append(status.id)

    # save the tweet IDs along with the text in a .csv file
    fileName = os.path.join(rootPath, 'data', target, 'status%s.csv'%today)
    statusTweets = pd.DataFrame(columns = ['id', 'text'])
    statusTweets['id'] = tweet_ids
    statusTweets['text'] = tweet_texts
    statusTweets.to_csv(fileName, index = False)        

    return tweet_texts, tweet_ids

def main():
    auth = login.main()
    targets = accountNames
    makeFolders(targets)

'''
Remove all irrelevant characters such as any non alphanumeric characters
Tokenize your text by separating it into individual words
Remove words that are not relevant, such as “@” twitter mentions or urls
Convert all characters to lowercase, in order to treat words such as “hello”, “Hello”, and “HELLO” the same
Consider combining misspelled or alternately spelled words to a single representation (e.g. “cool”/”kewl”/”cooool”)
Consider lemmatization (reduce words such as “am”, “are”, and “is” to a common form such as “be”)
'''