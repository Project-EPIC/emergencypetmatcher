"""
Twitter listener.
"""

import tweepy
from datetime import datetime
from gftclient.authorization.clientlogin import ClientLogin
from gftclient.sql.sqlbuilder import SQL
from gftclient import ftclient


CKEY = 'ssl0g9FopCG1zsItjarBJg'
CSEC = 'eDRctXylxlXxHuFQqrLSXcRtTkY1CVMpZtdaM46Wg'
AKEY = '397561453-Xq0bQ8BnDEH0jxE5gsjoGENdzjAOH1tLdMRS9dYt'
ASEC = 'NhUxMWPXv0jLQ6Sudivgz9QST1sXm8XDiR4pwPzFo'

class PetTweet():
    def __init__(self):
        self.pet_name = ""
        self.contact = ""
        self.tags = ""
        self.lost = ""
        self.found = ""
        self.latitude = ""
        self.longitude = ""
        self.photo = ""

    def __str__(self):
        return self.pet_name + " / " + self.contact + " / " + self.tags + " / " + self.lost + " / " + self.found + " / " + self.latitude + " / " + self.longitude + " / " + self.photo 

    def parse_tweet(self, tweet):
        terms = tweet.text.split()
        keywords = ["#pepicgft", "#name", "#found", "#lost", "#tags", "#contact", "#photo"]
        for term, index in zip(terms, range(len(terms))):
            try:
                if term in ("#name", "#tags", "#contact"):
                    x = index+1
                    buf = ""
                    while terms[x] not in keywords and x < len(terms) - 1:
                        buf = buf + terms[x] + " "
                        x = x + 1
                    if term == "#name":
                        print "Name is " + buf
                        self.name = buf
                    elif term == "#tags":
                        print "Tags are " + buf
                        self.tags = buf
                    elif term == "#contact":
                        print "Contact is " + buf
                        self.contact = buf
                elif term == "#found":
                    self.found = str(datetime.now())
                elif term == "#lost":
                    self.lost = str(datetime.now())
                elif term == "#photo":
                    self.photo = terms[index+1]
            except Exception as e:
                print e          
        if tweet.geo is not None:
            self.latitude = str(tweet.geo["coordinates"][0])
            self.longitude = str(tweet.geo["coordinates"][1])
        try:
            if self.photo == "":
                self.photo = str(tweet.entities["media"][0]["media_url_https"])
        except:
            self.photo = ""

    def submit_tweet(self):
        print "SUBMITTING TWEET"
        print self.photo
        username="epicdatascouts@gmail.com"
        password="crowdsourcing"
        token = ClientLogin().authorize(username, password)
        ft_client = ftclient.ClientLoginFTClient(token)
        tid = 2038141
        rowdata = {'Pet Name':str(self.name), 'Tags':str(self.tags), 'Contact':str(self.contact), "Latitude":str(self.latitude), "Longitude":str(self.longitude), "Lost":str(self.lost), "Found":str(self.found), "Photograph":str(self.photo)}
        try:
            ft_client.query(SQL().insert(tid, rowdata))
        except Exception as e:
            print e

class PetSWL(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tw = PetTweet()
            tw.parse_tweet(status)

            if tw is not None:
                tw.submit_tweet()
        except:
            pass

    def on_error(self, status_code):
        print "error"
        return True


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(CKEY, CSEC)
    auth.set_access_token(AKEY, ASEC)

    stream = tweepy.Stream(auth=auth, listener=PetSWL(), secure=True)
    stream.filter(track=("pepicgft",))

