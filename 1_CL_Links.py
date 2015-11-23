__author__ = 'martinrasumoff'

__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
import time
import random

# Connecting to the MongoDb at AWS
client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
print db
collection = db['Links_to_articles']
print collection
collection.create_index("link")

#Setting the starting point
starting_point =
url = 'http://buscar.lanacion.com.ar/corrupcion?sort=default&offSet=3900'

response = requests.get(url)

site_page = 1

while ((response.status_code == 200)):
    page = response.text
    soup = BeautifulSoup(page)

    print "Page:",site_page

    for link in soup.find_all('a'):
        has = link.get('onclick')
        if has != None:
            if 'http://www.lanacion.com.ar/' in has:
                start = has.find("'")
                end = has.find("'",start+1)
                article_link = has[start+1:end]

                # Only adding the link if it is not existent currently
                exist = collection.find_one({"link": article_link})
                if exist == None:
                    article_object = {"link":article_link,"source":"Clarin"}
                    article_id = collection.insert_one(article_object)
                    print 'Link added:',article_link
                else:
                    print 'Link passed:',article_link

    site_page += 1
    url = 'http://buscar.lanacion.com.ar/corrupcion?sort=default&offSet='+str(10*site_page)

    while True:
        try:
            response = requests.get(url)
        except ConnectionError:
            print "Oopss...we've been cut off... :( Let's take some time off :)"

        if response.status_code != 200:
            print "Sleeping..."
            time.sleep(12)
        else:
            break
