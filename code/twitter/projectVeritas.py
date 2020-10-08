
import os
import pandas as pd
import time
import tweepy

import loginPi
auth = loginPi.main()
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
    links = [
        ' https://www.newsbreak.com/news/2077040488191/project-veritas-alleged-ballot-harvester-says-he-was-offered-bribe-to-lie-about-ties-to-ilhan-omar',
        ' https://lawandcrime.com/high-profile/subject-of-project-veritas-voter-fraud-video-says-he-was-offered-10000-to-lie-about-ballot-harvesting-for-ilhan-omar/',
        ' https://www.fox9.com/news/subject-of-project-veritas-voter-fraud-story-says-he-was-offered-bribe'
    ]
    
    intros = [' Lies', ' False', ' Fake News', ' No', ' Incorrect', ' Wrong']
    punctuations = ['. ', '! ']
    tweetTexts = [
        'Subject of Veritas video offered bribe to defame Minnesotas Congresswoman Ilhan Omar. ',
        'Subject of Veritas video offered bribe to smear Minnesotas Congresswoman Ilhan Omar. '
    ]

    firstHalves = [intro + punctuation for intro in intros for punctuation in punctuations]
    secondHalves = [tweetText + link for tweetText in tweetTexts for link in links]
    output = [firstHalf + secondHalf for firstHalf in firstHalves for secondHalf in secondHalves]
    return output + output

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
    fullPath = os.path.join(rootPath, 'data/projectVeritas', fileName)
    df.to_csv(fullPath, index=False)
    return

def openArray(accomplishedList = True):

    fileName = 'completed.csv' if accomplishedList else 'failed.csv'
    fullPath = os.path.join(rootPath, 'data/projectVeritas', fileName)
    df = pd.read_csv(fullPath, header=0)

    return [(name, str(id)) for name, id in zip(df['names'].values, df['id'].values)]

def main():
    # open .csv file of already completed
    completed, failed = openArray(), openArray(False)

    # choose the tweet ID for the top of your tree
    # https://twitter.com/Project_Veritas/status/1313843538094968833
    # https://twitter.com/RealJamesWoods/status/1312176155852587009/photo/1
    # https://twitter.com/Project_Veritas/status/1312090956552982528
    # https://twitter.com/my3monkees/status/1313517274968600580
    # https://twitter.com/ConservaMomUSA/status/1310764598828707841
    # https://twitter.com/CTruthforTrump/status/1310792134153383936
    # https://twitter.com/TrumpCat04/status/1310983215570661376
    # https://twitter.com/justjohnPatriot/status/1310770840691245058
    # https://twitter.com/9NEWSNANCY/status/1310931168687132672
    # https://twitter.com/Dude4Liberty/status/1310950992930910216
    # https://twitter.com/JamesOKeefeIII/status/1311521262401810432
    # https://twitter.com/ChicagoDC6/status/1311044835974012930
    topOfTree = '1313843538094968833'

    completed, failed = responseTreeDepth1(topOfTree, completed, failed, 5)

    # save completed misinformation
    saveArray(completed)
    # save failed misinformation
    saveArray(failed, False)

if __name__== '__main__':
    main()
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