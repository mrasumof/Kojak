__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
import requests
import time

# Connecting to the MongoDb at AWS
client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
print db
coll_articles = db['Articles']
coll_links = db['Links_to_articles']
print coll_links
print coll_articles

counter = 1
total = coll_links.find({"source":"Clarin"}).count()

for each in coll_links.find({"source":"Clarin"}):

    #print "Gathering:"+each['link']
    article_link = each['link']

    #Check if the article exists in the DB
    exist = coll_articles.find_one({"link": article_link, "source":"Clarin"})

    if exist == None:

        while True:
            try:
                response = requests.get(article_link)
            except ConnectionError:
                print "Oopss...we've been cut off... :( Let's take some time off :)"

            if response.status_code != 200:
                print "Sleeping..."
                time.sleep(12)
            else:
                break

        page = response.text

        article_object = {"link":article_link, "article":page, "source:":"Clarin"}
        article_id = coll_articles.insert_one(article_object)

        print 'Link added:',article_link
    else:
        print 'Link passed:',article_link

    print "Total Processed:"+str(counter)+" of "+str(total)
    counter += 1

