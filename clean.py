import re

clean = []
def process(tweet):
         #global count
         #count = count+1 
         tweet = tweet.lower()
         tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)#Remove www.* or https?://*
         tweet = re.sub('@[^\s]+','',tweet)#Remove @username
         tweet = re.sub(r'[^\w\s]','',tweet)#Remove punctuation     
         tweet = " ".join(word.strip() for word in re.split('#|_', tweet))#Convert #word into word 
         tweet = re.sub('[0-9]+','',tweet)#Remove numbers
         tweet = re.sub('(xf[^\s]+)|(xe[^\s]+)','',tweet)#Remove emojis
         tweet = re.sub('^(rt)','',tweet)#Remove RT if they appear at the beginning of a tweet     
         clean.append(tweet)



filename = input("Filename:")
file = open(filename,'r',encoding = "utf-8")
text = file.read()
for i in text.split(','):
    process(i)
file.close()
out = input ("Output:")
file = open(out,'w',encoding = "utf-8")
file.write(str(clean))
file.close()
