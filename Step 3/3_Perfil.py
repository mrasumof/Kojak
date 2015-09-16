__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
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
total = coll_links.find({"source":"Perfil",'parsed':"N"}).count()

for each in coll_links.find({"source":"Perfil",'parsed':"N"}):

    article_link = each['link']

    if ((article_link[11] == u'p') and (article_link[7] == u'w')):
        # Only adding the article if it is not existent currently
        exist = coll_parsed.find_one({"link": article_link})
        if exist == None:

            print "Gathering:"+each['link']

            while True:
                try:
                    response = requests.get(article_link)
                except ConnectionError:
                    print "Oopss...we've been cut off... :( Let's take some time off :)"
                    print "Sleeping..."
                    print response.status_code
                    wait_time = random.uniform(1,15)
                    time.sleep(wait_time)
                else:
                    break

            page = response.text
            soup = BeautifulSoup(page)

            if soup.find('h1') is not None:
                if soup.find('h1').get("text") is not  None:
                    article_title = soup.find('h1').text
                else:
                    article_title = ''

                #if soup.find(class_='volanta').text is not None:
                #    article_volanta = soup.find(class_='volanta').text
                #else:
                article_volanta = ''

                if soup.find('h3').text is not None:
                    article_subtitl = soup.find('h3').text
                else:
                    article_subtitl = ''

                if soup.find(itemprop='articleBody').text is not None:
                    article_body = soup.find(itemprop='articleBody').text
                else:
                    article_body = ''

                #Date Parsing
                date_str = soup.find('time')['datetime']
                article_date = dateparser.parse(date_str)

                article_date_txt = date_str
                article_source = 'Perfil'

                article_object = {"link":article_link,\
                                  "title":article_title,\
                                  "volanta":article_volanta,\
                                  "subtitle":article_subtitl,\
                                  "body":article_body,\
                                  "date_txt":article_date_txt,\
                                  "date":article_date,\
                                  "source":article_source}

                article_id = coll_parsed.insert_one(article_object)
                ok_id = coll_links.update_one({"link":article_link },{"$set" : {"parsed":"Y"}})
                print 'Link added:',article_link
            else:
                ok_id = coll_links.update_one({"link":article_link },{"$set" : {"parsed":"Y"}})
                print 'Link passed:',article_link

    print "Total Processed:"+str(count)+" of "+str(total)
    count += 1
