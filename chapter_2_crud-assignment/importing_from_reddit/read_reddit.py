
import json
#import urllib2
import urllib
import pymongo
from urllib.request import urlopen

# connect to mongo
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the reddit database
db=connection.reddit
stories = db.stories

# drop existing collection
stories.drop()

# get the reddit home page
print("Opening Reddit Homepage")
#reddit_page = urllib2.urlopen("http://www.reddit.com/r/technology/.json")
#reddit_page = urlopen('file:///D:/MyData/Education/Computer%20Studies/MongoDB/M101%20MongoDB%20for%20Developers/Week2/chapter_2_crud/importing_from_reddit/reddit_1.json')

#reddit_page = urlopen("http://www.reddit.com/r/technology/.json")

reddit_page = urlopen('file:///D:/MyData/Education/Computer%20Studies/MongoDB/M101%20MongoDB%20for%20Developers/Week2/chapter_2_crud/importing_from_reddit/reddit.json')

# parse the json into python objects
#parsed = json.loads(reddit_page.read())
parsed = json.loads(reddit_page.read().decode('utf-8'))
print("Page Parsed")
# iterate through every news item on the page
for item in parsed['data']['children']:
    # put it in mongo
	#print((item['data']))
	#print("Inserting one doc")
    stories.insert_one(item['data'])




