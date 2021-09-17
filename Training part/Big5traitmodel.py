
#big5 trait model
#The support from IBM for personality insights are deprecated.Only IBM who provide for trained-
#-model packages and libraries.So we cannot run this.But this is backend of Personality insights.




import tweepy

from textblob import TextBlob

import pandas as pd

import re

import json

from ibm_watson import PersonalityInsightsV3

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator






consumerKey = 'ZSTjRgpSwrcpgLDqTug1tnHVS'

consumerSecret = '2mfFBHGIV0OT7b5LbgWrAbBhoyr3tB7GiGTtCGiz0pN8S9EFKv'

accessToken = '1014097837381111808-1ZmyTn9NwXhnlnH3rLJdjLg7WmwFTG'

accessTokenSecret = 'siiC7b529NpcGT8uwopjOaauSRZoUQdlN38mLL0gX2TLK'

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

authenticate.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(authenticate, wait_on_rate_limit=True)

posts = api.user_timeline(screen_name='', count=100, lang="en", tweet_mode="extended")



def cleanTxt(text):
    text = re.sub('@[A-Za-z0-9]+', '', text)

    text = re.sub('#', '', text)

    text = re.sub('\n', '', text)

    text = re.sub('RT[\s]+', '', text)

    text = re.sub('https?:\/\/\S+', '', text)

    return text

tweete=[]

for tweet in posts:

    tweets=tweet.full_text

    l=cleanTxt(tweets)

    tweete.append(l)

tweete = ' '.join([str(elem) for elem in tweete])

#print(tweete)

apikey= 'ZA4IIlrbFFCjJ-y_b0L7ugZOu9_CWW6J57951KTTnzWq'   #was removed by IBM

url= 'https://gateway-syd.watsonplatform.net/personality-insights/api'



authenticator=IAMAuthenticator(apikey)

personality_insights = PersonalityInsightsV3(

    version= '2017-10-13',

    authenticator=authenticator
)


personality_insights.set_service_url(url)

profile=personality_insights.profile(tweete,accept='application/json').get_result()

#printing the profile can see the rating of

#Extroversion.

#Neuroticism.

#Agreeableness.

#Conscientiousness.

#Openness.
