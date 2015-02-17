import requests
import feedparser
import praw
from bs4 import BeautifulSoup

r = praw.Reddit('/r/jailbreak package description bot')
r.login("username","password")

def checkType(link):
    response = requests.post(link)
    soup = BeautifulSoup(response.text)
    tag= soup.find(id="section")
    type = str(tag.string)
    if type == "Tweaks":
        return True
    else:
        return False
def checkTweak(packageName):        
    response = requests.post("http://planet-iphones.com/cydia/feed/name/" + packageName)
    feed = feedparser.parse( response.text )
    for item in feed[ "items" ]:
        title = item[ "title" ]
        if title.lower() == packageName:
            return True
        else:
            return False
    
def getTweak(packageName):        
    response = requests.post("http://planet-iphones.com/cydia/feed/name/" + packageName)
    feed = feedparser.parse( response.text )
    for item in feed[ "items" ]:
        title = item[ "title" ]
        if title.lower() == packageName:
            link = str(item[ "link" ])
            descrip = str(item[ "description" ])
            link = "http://cydia.saurik.com/package/" + link.replace("http://planet-iphones.com/cydia/id/", "")
            if checkType(link):
                return link, descrip
while True:
    subreddit = r.get_subreddit('jailbreak')
    for submission in subreddit.get_new(limit=25):
        obj = open('seen_posts.txt', 'ab+')
        if submission.id not in open("seen_posts.txt").read():
            title = submission.title
            for words in title.split(" "):
                if checkTweak(words.lower()):
                    link, descrip = getTweak(words.lower())
                    submission.add_comment("The following is short description and link to the tweak mentioned in this post: \n\n Title: [" + words +"](" + link + ") \n\nDescription: " + descrip + " \n\nCreated by healdb. This bot uses http://planet-iphones.com to find its information, and therefore makes no guarantees on it's accuracy")
                    print "Found post and commented, link: " + submission.permalink
        obj.write(submission.id)
        obj.close()
