__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
import time
import dateparser
import random

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']

coll_articles = db['Articles']
coll_links = db['Links_to_articles']
coll_parsed = db['Parsed_Articles']

print coll_links
print coll_articles
print coll_parsed

count = 1
total = coll_links.find({"source":"LaNacion","parsed":"N"}).count()

#b.inventory.find( { $and: [ { price: { $ne: 1.99 } }, { price: { $exists: true } } ] } )
for each in coll_links.find({"source":"LaNacion",'parsed':"N"}):

    article_link = each['link']

    # Only adding the article if it is not existent currently
    exist = coll_parsed.find_one({"link": article_link})
    if exist == None:

        print "Gathering:"+each['link']

        while True:
            try:
                response = requests.get(article_link)
            except ConnectionError:
                print "Oopss...we've been cut off... :( Let's take some time off :)"
                print response.status_code
                wait_time = int(random.uniform(1, 15))
                print "Sleeping..."+str(wait_time)+" seconds"
                time.sleep(wait_time)
            else:
                break

        page = response.text
        soup = BeautifulSoup(page)

        if soup.find('h1').text !=  None:
            article_title = soup.find('h1').text.encode('latin1').decode('utf8')
        else:
            article_title = ''

        if soup.find(class_='volanta').text != None:
            article_volanta = soup.find(class_='volanta').text.encode('latin1').decode('utf8')
        else:
            article_volanta = ''

        if soup.find(class_='bajada').text != None:
            article_subtitl = soup.find(class_='bajada').text.encode('latin1').decode('utf8')
        else:
            article_subtitl = ''

        if soup.find(id='cuerpo').text != None:
            article_body = soup.find(id='cuerpo').text.encode('latin1').decode('utf8')
        else:
            article_body = ''

        #Date Parsing
        date_str = soup.find(class_='fecha')['content'].encode('latin1').decode('utf8')
        article_date = dateparser.parse(date_str)

        article_date_txt = date_str
        article_source = 'LaNacion'

        article_object = {"link":article_link,\
                          "title":article_title,\
                          "volanta":article_volanta,\
                          "subtitle":article_subtitl,\
                          "body":article_body,\
                          "date_txt":article_date_txt,\
                          "date":article_date,\
                          "source":article_source}

        article_id = coll_parsed.insert_one(article_object)
        ok_id = coll_links.update_one({"link":article_link},{"$set" : {"parsed":"Y"}})
        print 'Link added:',article_link
    else:
        ok_id = coll_links.update_one({"link":article_link},{"$set" : {"parsed":"Y"}})
        print 'Link passed:',article_link

    print "Total Processed:"+str(count)+" of "+str(total)
    count += 1
