from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import re
import ast
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import random

from kivy.app import App
from kivy.uix.label import Label
#from kivy.core.window import Window



from nltk.corpus import PlaintextCorpusReader
import nltk.classify.util
from nltk.corpus import PlaintextCorpusReader
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

class abc(username):
    
consumer_key = "D9idPsR9iCUbzQzlUIoOUlOjc"
consumer_secret = "VGLhthlGLxbJpPyu3WtTTz4oKLYYkJ5VHJIn94Azf0bDoeE7vm"
access_token = "798166878-qgZxk593TZpoSpaZyPBMI1wnOjkKH80AFGR0ZqAg"
access_token_secret = "DvQDsAEGm23yG6aRVoPhrVIeZINR6Y47jgjdXgdF7OaVH"
     
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

target = username



rel = ['hate', 'left', 'bf','gf','girlfriend','boyfriend','heartbreak','alone', 'love','abuse']
edu = ['exam','test','assignment','school','studying']
mon = ['broke','money','cash','economy', 'finance','crisis']

cleantweet = []
clist = []
text = []
mylist = []
words = []
global dcount,Money
dcount = 0
Money = 0
global ccount,Academic
ccount = 0
Academic = 0
global tcount,Relationship
tcount = 0
Relationship = 0
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
random.shuffle(train_set)
test_set =  neg_re[45:] + pos_re[45:]
random.shuffle(test_set)

#print(len(train_set),len(test_set))
classifier = NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.util.accuracy(classifier, test_set)
#print(accuracy * 100)

class Helpline(App):
    def build(self):
        #Window.clearcolor = (0.50,0.50,0.50,1)
        return  Label(text="Need to talk to someone? \n\nNational Suicide Helpline \n\nVisit: http://www.aasra.info/ \nCall: +912227546669 \n\nWant to chat with a counsellor? \nVisit:https://yourdost.com/")
hp=Helpline()
def get_info(target):
   try: 
    item = auth_api.get_user(target)
    print("Name: " + item.name)
    print("Twitter name: " + item.screen_name)
    print("Total number of times tweeted: " + str(item.statuses_count))
    if (item.statuses_count < 50):
        print ("Insufficient Data to analyse")
        exit()
    print("Following: " + str(item.friends_count))
    print("Followers: " + str(item.followers_count))
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

def get_cause(clist):
    global Relationship,Academic,Money
    for w in clist:
        if w in rel:
            Relationship+=1
        elif w in edu:
            Academic+=1
        elif w in mon:
            Money+=1
   

def get_classify(tweet):
    clist = []
    global dcount
    global ccount
    words = word_tokenize(tweet)
    clist = words[:]
    get_cause(clist)
    words = create_word_features(words)
    x=classifier.classify(words)
    if x == "Depressed":
        dcount+=1
    else:
        ccount+=1
  

     
get_info(target)
try:
 get_tweets(target)
except:
    print("%s's account is set to private" % target)
    exit()
for tweet in mylist:
    
    tcount+=1
    tweet = tweet.replace('"','')
    tweet = tweet.lower()
    tweet = re.sub('^rt','',tweet)#Remove RT if they appear at the beginning of a tweet
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)#Remove www.* or https?://*
    tweet = re.sub('@[^\s]+','',tweet)#Remove @username
    tweet = " ".join(word.strip() for word in re.split('#|_', tweet))#Convert #word into word 
    tweet = re.sub('[0-9]+','',tweet)#Remove numbers
    tweet = re.sub(r'[^\w\s]','',tweet)#Remove punctuation
    tweet = re.sub('[\s]+',' ', tweet)#Remove additional white spaces
    cleantweet.append(tweet)
    get_classify(tweet)


def biggest(a, y, z):
    Max = a
    if y > Max:
        Max = y    
    if z > Max:
        Max = z
        if y > z:
            Max = y
    return Max

    
tot = dcount+ccount
#print(dcount,ccount)
rat = dcount/tot
print (rat)
if (rat < 0.25 ):
    print (" %s is unlikely to be depressed" % target)
elif (rat > 0.25 and rat < 0.4):
    print (" %s is likely to be moderately depressed" % target)
    cause = biggest(Relationship,Money,Academic)
    if (cause == Relationship):
     print("Cause for depression is likely to be relationship troubles")
    elif (cause == Money):
     print("Cause for depression is likely to be money troubles")
    elif (cause == Academic):
     print ("Cause for depression is likely to be academic troubles")
else:
    hp.run()
    print ("%s is likely to be severely depressed" % target)
    cause = biggest(Relationship,Money,Academic)
    if (cause == Relationship):
     print("Cause for depression is likely to be relationship troubles")
    elif (cause == Money):
     print("Cause for depression is likely to be money troubles")
    elif (cause == Academic):
     print ("Cause for depression is likely to be academic troubles")
    

with open("%s.txt" % target,'w',encoding = 'utf-8') as f:
    f.write(str(cleantweet))
f.close()    

def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = int(360.0 * 45.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)   
file_content=open ("%s.txt" % target).read()
wordcloud = WordCloud(font_path = r'C:\Windows\WinSxS\amd64_microsoft-windows-font-truetype-verdana_31bf3856ad364e35_10.0.16299.15_none_e1654f127052576a\verdana.ttf',                            stopwords = STOPWORDS,
                            background_color = 'white',
                            width = 1200,
                            height = 1000,
                            color_func = random_color_func,
                            collocations = False
                            ).generate(file_content)

plt.imshow(wordcloud)
plt.axis('off')
plt.show()

class LoginApp(App):
    username = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))

        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    LoginApp().run()
