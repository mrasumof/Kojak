__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
import dateparser
import random
import time


client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']

coll_articles = db['Articles']
coll_links = db['Links_to_articles']
coll_parsed = db['Parsed_Articles']

print coll_links
print coll_articles
print coll_parsed

count = 1
total = coll_links.find({"source":"Infobae",'parsed':"N"}).count()

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36"

for each in coll_links.find({"source":"Infobae",'parsed':"N"}):

    article_link = each['link']

    if (('/opinion.infobae.com' not in article_link) and ('/blogs.infobae.com' not in article_link)):

        # Only adding the article if it is not existent currently
        exist = coll_parsed.find_one({"link": article_link})
        if exist == None:

            print "Gathering:"+each['link']

            while True:
                try:
                    response = requests.get(article_link, headers={'User-Agent': agent})
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

            if soup.find(class_='entry-title') is not None:
                article_title = soup.find(class_='entry-title').text
            else:
                article_title = ''

            if soup.find(class_='cat cat-') is not None:
                if soup.find(class_='cat cat-').get('data-header-tag') is not None:
                   article_volanta = soup.find(class_='cat cat-')['data-header-tag']
                else:
                    article_volanta = ''
            else:
                article_volanta = ''

    #        if soup.find('h3').text is not None:
    #            article_subtitl = soup.find('h3').text
    #        else:
            article_subtitl = ''

            if soup.find(class_='cuerposmart clearfix') is not None:
                article_body = soup.find(class_='cuerposmart clearfix').text
            else:
                article_body = ''

            #Date Parsing
            date_str = soup.find(class_='hide pubdate updated').text
            article_date = dateparser.parse(date_str)

            article_date_txt = date_str
            article_source = 'Infobae'

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
