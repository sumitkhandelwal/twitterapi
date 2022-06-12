from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import userinput
import tweepy
from textblob import TextBlob

def secreteDetails():
    consumer_key = 'b5louio5EgmlvE6p4JljVGoHa'
    consumer_secret = 'qlWPqrdt3PHUZO1hOBoVTIfKC2IeVW1KSabtnheNIXUHag3leM'
    access_token = '1519713038240448512-0a61lfwDlBvt9W8GJhCrGFBt7NKNx6'
    access_token_secret = 'PSWbty9gZE5IPsJ0UoxpKn50aScrVFyTUpZv7Rc7IVVeB'
    return consumer_key, consumer_secret, access_token, access_token_secret

def primary(input_hashtag):
    consumer_key, consumer_secret, access_token, access_token_secret = secreteDetails() #secrets imported from secrets.py
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    N = 100                         #Number of Tweets
    Tweets = tweepy.Cursor(api.search_tweets, q=input_hashtag).items(N)
    #print(Tweets)
    neg = 0.0
    pos = 0.0
    neg_count = 0
    neutral_count = 0
    pos_count = 0
    tweetData = []
    sentiment = []
    for tweet in Tweets:
        #print (tweet.text)
        tweetData.append(tweet.text)
        blob = TextBlob(tweet.text)
        if blob.sentiment.polarity < 0:         #Negative
            neg += blob.sentiment.polarity
            neg_count += 1
            sentiment.append('Negative')
        elif blob.sentiment.polarity == 0:      #Neutral
            neutral_count += 1
            sentiment.append('Neutral')
        else:                                   #Positive
            pos += blob.sentiment.polarity
            pos_count += 1
            sentiment.append('Positive')

    tweetData = zip(tweetData, sentiment)
    return [['Sentiment', 'no. of tweets'],['Positive',pos_count]
            ,['Neutral',neutral_count],['Negative',neg_count]], tweetData

def index(request):
    user_input = userinput()
    return render(request, "index.html", {'input_hastag': user_input})

def analyse(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        print (input_hastag)
        data, tweetData = primary(input_hastag)
        print(data)
        return render(request, "result.html", {'data': data, 'tweetData': tweetData})
    return render(request, "index.html", {'input_hastag': user_input})