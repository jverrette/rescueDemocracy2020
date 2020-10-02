
import os
import pandas as pd
import time
import tweepy

import login
auth = login.main()
api = tweepy.API(auth)

'''
get id and account name of actual tweet
target = 'Cernovich'
statusID = '1311904974532567040'
'''
rootPath = '/home/jean/Documents/rescueDemocracy2020'

def reply(replyText, originalReTweet):
    fullText = '@' + originalReTweet.user.screen_name + replyText
    try:
        t = api.update_status(status=fullText, in_reply_to_status_id=originalReTweet.id, auto_populate_reply_metadata=True)
        print('sucess with: ' + originalReTweet.user.screen_name)
        #completed(originalReTweet.user.screen_name)
        return True
    except:
        print('failed with: ' + originalReTweet.user.screen_name)
        return False
    time.sleep(15)

# Create a large number of responses.
def generateResponses():
    link = ' https://thehill.com/homenews/media/519315-wapo-removes-imagine-to-never-have-to-think-about-president-trump-again'
    intros = [' Lies', ' False', ' Fake News', ' No', ' Incorrect', ' Wrong']
    punctuations = ['. ', '! ']
    washingtonPosts = [
        'Original tweet is title of WPost article written at 3:30pm EST or 12:30pm PDT on Oct 1. ',
        'Original tweet is title of WPost article written 10 hours before Trump tweeted he tested positive. ',
        'Original tweet is title of WPost article written at 3:30pm EST or 12:30pm PDT on Oct 1! ',
        'Original tweet is title of WPost article written 10 hours before Trump tweeted he tested positive! '
    ]

    endings = ['Its about voting Trump out!', 'Its about voting Trump out.']
    firstHalves = [intro + punctuation for intro in intros for punctuation in punctuations]
    secondHalves = [washingtonPost + ending for washingtonPost in washingtonPosts for ending in endings]
    return [firstHalf + secondHalf + link for firstHalf in firstHalves for secondHalf in secondHalves]

def responseTreeDepth1(statusID, completed, failed, counts = 100):
    try:
        results = api.retweets(statusID, counts)
    except:
        print('Problem collecting retweets')

    responses = generateResponses()
    iterations = min(len(results), len(responses))

    namesCompleted = [el[0] for el in completed]

    for response, originalReTweet in zip(responses[:iterations], results[:iterations]):
        currentReTweet = (originalReTweet.user.screen_name, str(originalReTweet.id))
        if currentReTweet[0] not in namesCompleted:
            outputCode = reply(response, originalReTweet)

            # keep track of what misinformation has already been responded to
            if outputCode:
                completed.append(currentReTweet)
            else:
                failed.append(currentReTweet)
    return completed, failed

def saveArray(array, accomplishedList = True):
    df = pd.DataFrame()
    df['names'] = [el[0] for el in array]
    df['id'] = [el[1] for el in array]

    fileName = 'completed.csv' if accomplishedList else 'failed.csv'
    fullPath = os.path.join(rootPath, 'data/washingtonPost', fileName)
    df.to_csv(fullPath, index=False)
    return

def openArray(accomplishedList = True):

    fileName = 'completed.csv' if accomplishedList else 'failed.csv'
    fullPath = os.path.join(rootPath, 'data/washingtonPost', fileName)
    df = pd.read_csv(fullPath, header=0)

    return [(name, str(id)) for name, id in zip(df['names'].values, df['id'].values)]

def main():
    # open .csv file of already completed
    completed, failed = openArray(), openArray(False)

    # choose the tweet ID for the top of your tree
    topOfTree = '1311904974532567040'

    completed, failed = responseTreeDepth1(topOfTree, completed, failed)

    # save completed misinformation
    saveArray(completed)
    # save failed misinformation
    saveArray(failed, False)

'''
Link to article
https://www.washingtonpost.com/opinions/imagine-what-it-will-be-like-to-never-have-to-think-about-trump-again/2020/10/01/d0b32de0-0413-11eb-a2db-417cddf4816a_story.html?tid=ss_tw 
'''

'''
StevenHeinrich_
1311961212326875136
_Erva___
1311960687422435328
nawilliams34
1311960438658273281
RubyBelvin
1311960273532706816
jeffy202020
1311960267203510272
gattling
1311960160173203456
DekeKahala
1311959989972590592
ChrisFlaank
1311959625357549568
BrianCa62811383
1311959544105439233
theblakeblazes
1311959328534953985
RanHarpaz
1311959058707079171
LewP
1311958969884254210
RebelRightous
1311958914884345858
mmiittuusshhii
1311958691785003008
politicachica76
1311958647057059841
truSBL
1311958627897487360
3iwa
1311958564848635906
H777Is
1311958514697482240
NBfromLB
1311957707268685824
'''