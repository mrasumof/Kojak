__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
import time

# Connecting to the MongoDb at AWS
client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
print db
collection = db['Links_to_articles']
print collection
collection.create_index("link")

#Setting the starting point
starting_point = 0
# 'compra%20de%20votos'
url = "http://buscar.lanacion.com.ar/clientelismo?sort=default&offSet=0"

response = requests.get(url)

site_page = 1
total_added = 0

while ((response.status_code == 200)):
    page = response.text
    soup = BeautifulSoup(page)

    print "Page:",site_page

    flag = 0

    for link in soup.find_all('a'):

        flag = 1

        has = link.get('onclick')
        if has != None:
            if 'http://www.lanacion.com.ar/' in has:
                start = has.find("'")
                end = has.find("'",start+1)
                article_link = has[start+1:end]
                article_source = "LaNacion"

                # Only adding the link if it is not existent currently
                exist = collection.find_one({"link": article_link})
                if exist == None:
                    article_object = {"link":article_link, "source":article_source}
                    article_id = collection.insert_one(article_object)
                    total_added += 1
                    print 'Link added:',article_link
                    print 'Total added:',str(total_added)
                else:
                    print 'Link passed:',article_link

    url = "http://buscar.lanacion.com.ar/clientelismo?sort=default&offSet="+str(10*site_page)
    site_page += 1

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

print 'Grand Total added:',str(total_added)
