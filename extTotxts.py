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


consumer_key = "D9idPsR9iCUbzQzlUIoOUlOjc"
consumer_secret = "VGLhthlGLxbJpPyu3WtTTz4oKLYYkJ5VHJIn94Azf0bDoeE7vm"
access_token = "798166878-qgZxk593TZpoSpaZyPBMI1wnOjkKH80AFGR0ZqAg"
access_token_secret = "DvQDsAEGm23yG6aRVoPhrVIeZINR6Y47jgjdXgdF7OaVH"
     
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

target = input("Username :")
text = []
mylist = []
words = []
global dcount
dcount = 0
global ccount
ccount = 0
long_stop_list = ['a','are','be','an','and','at','by','the','is','this','that','to','for','it','in','on']

def create_word_features(clist):
    useful_words = [word for word in clist if word not in long_stop_list]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

corpus_root = 'C:/Users/Bindu/Desktop/samp1/neg'
wordlists=PlaintextCorpusReader(corpus_root,'.*')
neg_re=[]
mylist=[]
x=[]
for fileids in wordlists.fileids():
    words = wordlists.words(fileids)
    neg_re.append((create_word_features(words),"Depressed"))

corpus_root='C:/Users/Bindu/Desktop/samp1/pos'  
wordlists=PlaintextCorpusReader(corpus_root,'.*')
pos_re=[]
mylist=[]
x=[]
for fileids in wordlists.fileids():
    words = wordlists.words(fileids)
    pos_re.append((create_word_features(words),"Not depressed"))

train_set = neg_re[:45] + pos_re[:45]
test_set =  neg_re[45:] + pos_re[45:]
print(len(train_set),len(test_set))
classifier = NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.util.accuracy(classifier, test_set)
print(accuracy * 100)



def get_info(target):
   try: 
    item = auth_api.get_user(target)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("statuses_count: " + str(item.statuses_count))
    if (item.statuses_count < 50):
        print ("Insufficient Data to analyse")
        exit()
    print("friends_count: " + str(item.friends_count))
    print("followers_count: " + str(item.followers_count))
    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))
    if account_age_days > 0:
        print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))    
   except:
        print ("Invalid Username")
        exit()
def get_tweets(target):
        
        print ("Collecting user %s's tweets" % target)
        for status in Cursor(auth_api.user_timeline, screen_name = '@%s' % target).items():
          mylist.append(json.dumps(status._json['text']))


def get_classify(tweet):
    global dcount
    global ccount
    words = word_tokenize(tweet)
    words = create_word_features(words)
    x=classifier.classify(words)
    if x == "Depressed":
        dcount+=1
    else:
        ccount+=1

    print(x) 
get_info(target)
get_tweets(target)
for tweet in mylist:
    tweet = tweet.replace('"','')
    tweet = tweet.lower()
    tweet = re.sub('^rt','',tweet)#Remove RT if they appear at the beginning of a tweet
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)#Remove www.* or https?://*
    tweet = re.sub('@[^\s]+','',tweet)#Remove @username
    tweet = " ".join(word.strip() for word in re.split('#|_', tweet))#Convert #word into word 
    tweet = re.sub('[0-9]+','',tweet)#Remove numbers
    #tweet = re.sub(r'(\u[^\s]+)','',tweet)#Remove emojis
    tweet = re.sub(r'[^\w\s]','',tweet)#Remove punctuation
    tweet = re.sub('[\s]+',' ', tweet)#Remove additional white spaces
 
    print (tweet)
    get_classify(tweet)

print(dcount,ccount)
   
