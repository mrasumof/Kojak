 #!/usr/local/bin/python

from pymongo import MongoClient
from bson.son import SON
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import random
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']
chrome = webdriver.Chrome()

tot_intern = 0
tot_records = coll_parsed.find({"thumbnail":"N"}).count()

for each in coll_parsed.find({"thumbnail":"N"}):
    article_link = each['link']

    while True:
        try:
            response = chrome.get(each['link'])
        except ConnectionError:
            print "Oopss...we've been cut off... :( Let's take some time off :)"
            print "Sleeping..."
            print response.status_code
            wait_time = random.uniform(1,15)
            time.sleep(wait_time)
        else:
            article_thumb = "thmb"+str(tot_intern)+".png"
            try:
                article_thumbnail = chrome.get_screenshot_as_file("/Users/martinrasumoff/Desktop/metis/screenshots/"+article_thumb)
            except ConnectionError:
                print "Oopss...we've been cut off... :( Let's take some time off :)"
                print "Sleeping..."
                print response.status_code
                wait_time = random.uniform(1,15)
                time.sleep(wait_time)
            else:
                ok_id = coll_parsed.update({"link":article_link},{"$set":{"thumbnail":"Y", "thumb_location":article_thumb}})
                break

    tot_intern +=1
    print "Total International: ",str(tot_intern)+" - "+article_link
