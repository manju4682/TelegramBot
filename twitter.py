import tweepy
from twittercredentials import oauth
import urllib
import json

def fetch_tweets():
    credentials = oauth()
    auth = tweepy.OAuthHandler(credentials['consumer_key'],credentials['consumer_secret'])
    auth.set_access_token(credentials['token_key'],credentials['token_secret'])
    api = tweepy.API(auth)
    fetch = tweepy.Cursor(api.search,q="'covid' 'bangalore' 'help' 'bed'",tweet_mode="extended").items(100)
    cnt = 1
    message = ""
    
    for i in fetch:
        if 'retweeted_status' in i._json:
            continue
        else:
            message += str(cnt)
            message += '\n'
            message += urllib.parse.quote(i.full_text)
            message += '\n'
            message += urllib.parse.quote(str(i.created_at))
            message += '\n\n'
            cnt+=1
        if(cnt==5): break    

    return message  
