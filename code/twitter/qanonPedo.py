import csv
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

badWords = [
    'savethechildren',
    'savethechildrenworldwide',
    'childtrafficking',
    'lolitaexpress',
    'wwg1gwaw',
    'saveourchildren',
    '10daysofdarkness',
    'wwg1gwa',
    'qanon2020',
    'trusttheplan',
    'followthewhiterabbit',
    'greatawakeningworldwide',
    'redoctober',
    'pedophile',
    'pedophilia',
    'child predator']

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
#    'Minnesota',
states = [
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

'''
get replies to a particular person, regardless of the story or original post
'''
def respondBadReplies(targetId):
    user = api.get_user(targetId)

    query = 'to:user.screen_name ' + ' OR '.join(badWords)
    for tweet in tweepy.Cursor(api.search,q='@'+user.screen_name, count = 10, result_type='recent', tweet_mode='extended'):
        if any([el in tweet.text.lower() for el in badWords]):
            # post a random of the responses to a bad tweet
            replyText = responses[random.randrange(0, 25)]
            reply(replyText, tweet)

    return

# open twitter IDs for a single state
# Iterate through each

def main():
    for state in states:
        print(state)
        userIds = accountNames(state)
        for i, userId in enumerate(userIds):
            print(i)
            try:
                spamMeme(userId)
            except:
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