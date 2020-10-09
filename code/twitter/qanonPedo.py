import csv
import datetime
import os
import pandas as pd
import random
import time
import tweepy

import loginJaro
auth = loginJaro.main()
api = tweepy.API(auth)

rootPath = '/home/jean/Documents/rescueDemocracy2020'
folderPath = os.path.join(rootPath, 'memes')
memes = [os.path.join(folderPath, f) for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]


statesFile = os.path.join(rootPath, 'data/qanon', 'states.csv')
states = pd.read_csv(statesFile)
# df.columns Index(['State', 'Abbreviation'], dtype='object')

badWords = [
    'SaveTheChildren',
    'ChildTrafficking',
    'LolitaExpress',
    'WWG1GWAW',
    'SaveOurChildren',
    '10daysofdarkness',
    'WWG1GWA',
    'QAnon2020',
    'TrustThePlan',
    'FollowTheWhiteRabbit',
    'GreatAwakeningWorldwide']

responses = ["Republican legislative aide Howard L. Brooks was charged with molesting a 12-year old boy and possession of child pornography.",
"Republican Senate candidate John Hathaway was accused of having sex with his 12-year old baby sitter and withdrew his candidacy after the allegations were reported in the media.",
"Republican preacher Stephen White, who demanded a return to traditional values, was sentenced to jail after offering $20 to a 14-year-old boy for permission to perform oral sex on him.",
"Republican anti-abortion activist Howard Scott Heldreth is a convicted child rapist in Florida.",
"Republican County Commissioner David Swartz pleaded guilty to molesting two girls under the age of 11 and was sentenced to 8 years in prison.",
"Republican judge Mark Pazuhanich pleaded no contest to fondling a 10-year old girl and was sentenced to 10 years probation.",
"Republican anti-abortion activist Nicholas Morency pleaded guilty to possessing child pornography on his computer and offering a bounty to anybody who murders an abortion doctor.",
"Republican legislator Edison Misla Aldarondo was sentenced to 10 years in prison for raping his daughter between the ages of 9 and 17.",
"Republican Mayor Philip Giordano is serving a 37-year sentence in federal prison for sexually abusing 8- and 10-year old girls.",
"Republican campaign consultant Tom Shortridge was sentenced to three years probation for taking nude photographs of a 15-year old girl.",
"Republican racist pedophile and United States Senator Strom Thurmond had sex with a 15-year old black girl which produced a child.",
"Republican pastor Mike Hintz, whom George W. Bush commended during the 2004 presidential campaign, surrendered to police after admitting to a sexual affair with a female juvenile.",
"Republican legislator Peter Dibble pleaded no contest to having an inappropriate relationship with a 13-year-old girl.",
"Republican activist Lawrence E. King, Jr. organized child sex parties at the White House during the 1980s.",
"Republican lobbyist Craig J. Spence organized child sex parties at the White House during the 1980s.",
"Republican Congressman Donald Buz Lukens was found guilty of having sex with a female minor and sentenced to one month in jail.",
"Republican fundraiser Richard A. Delgaudio was found guilty of child porn charges and paying two teenage girls to pose for sexual photos.",
"Republican activist Mark A. Grethen convicted on six counts of sex crimes involving children.",
"Republican activist Randal David Ankeney pleaded guilty to attempted sexual assault on a child.",
"Republican Congressman Dan Crane had sex with a female minor working as a congressional page.",
"Republican activist and Christian Coalition leader Beverly Russell admitted to an incestuous relationship with his step daughter.",
"Republican governor Arnold Schwarzenegger allegedly had sex with a 16 year old girl when he was 28.",
"Republican congressman and anti-gay activist Robert Bauman was charged with having sex with a 16-year-old boy he picked up at a gay bar.",
"Republican Committee Chairman Jeffrey Patti was arrested for distributing a video clip of a 5-year-old girl being raped.",
"Republican activist Marty Glickman (a.k.a. Republican Marty), was taken into custody by Florida police on four counts of unlawful sexual activity with an underage girl and one count of delivering the drug LSD."]

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

# create array consisting of all target twitter accounts
def accountNames(state):
    fileName = os.path.join(rootPath, 'data/twitterUsers', 'twitter%s.csv'%state)
    with open(fileName, newline='') as f:
        content = f.readlines()
    return [name.rstrip('\n') for name in content]

# Get a list of recent tweets from news site
# check responses for misinformation

def spamMeme(targetId):
    user = api.get_user(targetId)

    query = 'from:%s '%user.screen_name + ' Trump'
    for tweet in tweepy.Cursor(api.search,q=query, count = 10, result_type='recent', tweet_mode='extended').items(1):

        # post a random of the responses to a bad tweet
        replyImage = memes[random.randrange(0, len(memes))]
        # Upload image
        media = api.media_upload(replyImage)
 
        # Post tweet with image
        post_result = api.update_status(status="#VoteHimOut", media_ids=[media.media_id], in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)

    time.sleep(15)
    return

def replyBadTweet(targetId):

    # post a random of the responses to a bad tweet
    republicanPedo = responses[random.randrange(0, len(responses))]
 
    # Post tweet with image
    post_result = api.update_status(status=republicanPedo, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)

    print('Response sent to Republican: Wait 15 seconds')
    time.sleep(15)
    return

def saveArray(array, accomplishedList = True):
    df = pd.DataFrame()
    df['names'] = [el[0] for el in array]
    df['id'] = [el[1] for el in array]

    fileName = 'completed.csv' if accomplishedList else 'todo.csv'
    fullPath = os.path.join(rootPath, 'data/qanon', fileName)
    df.to_csv(fullPath, index=False)
    return

def openArray(accomplishedList = True):

    fileName = 'completed.csv' if accomplishedList else 'todo.csv'
    fullPath = os.path.join(rootPath, 'data/qanon', fileName)
    df = pd.read_csv(fullPath, header=0)

    return [(name, str(id)) for name, id in zip(df['names'].values, df['id'].values)]

# checks whether user is located in the united states or not
def inUSA(user):
    locationString = user.location
    '''
    # include users without the location attribute specified
    if not locationString:
        return True
    '''

    strings = [el.strip() for el in locationString.split(',')]
    for string in strings:
        if string.lower() in [el.lower() for el in ['US', 'USA', 'United States of America', 'USofA', 'America']]:
            return True
        #'State', 'Abbreviation'
        if string.lower() in [el.lower() for el in states['State'].values]:
            return True
        if string.lower() in [el.lower() for el in states['Abbreviation'].values]:
            return True

    return False

'''
get replies to a particular person, regardless of the story or original post
'''
def getBadTweets(todo, minTime, maxTime):

    query = ' OR '.join(['#'+badword for badword in badWords])

    # collect as many tweets with qanon hashtags as possible
    pages = tweepy.Cursor(api.search, q=query, count = n, tweet_mode='extended', since = minTime.strftime('%Y-%m-%d'), until = maxTime.strftime('%Y-%m-%d')).pages()
    print('Search Done')
    for page in pages:
        tweetPerPage = 0
        for tweet in page:
            tweetPerPage += 1
        
    #180*100 = 18k tweets per 15 minutes
    # To exceed the 5000-per-hour rate limit, 
    # you'd need to be doing at least 83 calls per minute or 1.4 calls per second.
    # restrict to tweets that are replies
            try:
                user = api.get_user(tweet.in_reply_to_user_id)
            
                # restrict to tweets that reply to a tweet from a user with many followers
                if (user.followers_count > 1000) & (inUSA(user)):
                    todo.append((tweet.author.screen_name, tweet.id))
                    replyBadTweet(tweet.id)
            except:
                pass
        print('Tweets per Page: %d'%tweetPerPage)

    return todo
'''
        # restrict to tweets that are replies
        try:
            user = api.get_user(tweet.in_reply_to_user_id)
            
            # restrict to tweets that reply to a tweet from a user with many followers
            if user.followers_count > 1000:
                todo.append((tweet.author.screen_name, tweet.id))
        except:
            pass
'''

'''
[('Davros_J_Slave', 1314298598574755840),
 ('JungleRedNM', 1314293842321924096),
 ('KnieriemLisa', 1314292450165284864),
 ('reidbianco', 1314291096764084224),
 ('1007julie', 1314290507900739590),
 ('TheMorrigan47', 1314279449307746306),
 ('SwifuFN', 1314279308332916736),
 ('uncommonlag', 1314276964404850688),
 ('sweetsgrandma', 1314271481921179649),
 ('KemiOlunloyo', 1314264030522101761)]
'''


# open twitter IDs for a single state
# Iterate through each

def main():
    '''
    for state in states:
        print(state)
        userIds = accountNames(state)
        for i, userId in enumerate(userIds):
            print(i)
            try:
                spamMeme(userId)
            except:
                time.sleep(900)
    '''
    todo = openArray(False)
    maxTime = datetime.datetime.now()
    minTime = maxTime - datetime.timedelta(hours=24, minutes=0)

    while True:
        try:
            todo = getBadTweets(todo, minTime, maxTime)
            saveArray(todo, False)
            minTime = minTime - datetime.timedelta(hours=24, minutes=0)
            maxTime = maxTime - datetime.timedelta(hours=24, minutes=0)

        except:
            print('Too many requests: Wait 15 minutes')
            time.sleep(900)

if __name__== '__main__':
    main()
'''
Remove all irrelevant characters such as any non alphanumeric characters
Tokenize your text by separating it into individual words
Remove words that are not relevant, such as “@” twitter mentions or urls
Convert all characters to lowercase, in order to treat words such as “hello”, “Hello”, and “HELLO” the same
Consider combining misspelled or alternately spelled words to a single representation (e.g. “cool”/”kewl”/”cooool”)
Consider lemmatization (reduce words such as “am”, “are”, and “is” to a common form such as “be”)
'''