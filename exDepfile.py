from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import re
import ast
import json


from nltk.corpus import PlaintextCorpusReader
import nltk.classify.util
from nltk.corpus import PlaintextCorpusReader
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

i = 1
mylist = []
consumer_key = "D9idPsR9iCUbzQzlUIoOUlOjc"
consumer_secret = "VGLhthlGLxbJpPyu3WtTTz4oKLYYkJ5VHJIn94Azf0bDoeE7vm"
access_token = "798166878-qgZxk593TZpoSpaZyPBMI1wnOjkKH80AFGR0ZqAg"
access_token_secret = "DvQDsAEGm23yG6aRVoPhrVIeZINR6Y47jgjdXgdF7OaVH"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


def get_tweets(target):
    with open("%s.txt" % target,'w',encoding = 'utf-8') as f:
     for status in Cursor(auth_api.user_timeline, screen_name = '@%s' % target).items():
             mylist.append((status._json['text']))
     f.write(str(mylist))        
        
for i in sys.argv:
    if i not in sys.argv[0]:
        get_tweets(i)
        
print("All done")    

    
