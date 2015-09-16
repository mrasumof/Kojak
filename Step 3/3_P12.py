__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
import dateparser


client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']

coll_articles = db['Articles']
coll_links = db['Links_to_articles']
coll_parsed = db['Parsed_Articles']

print coll_links
print coll_articles
print coll_parsed

count = 1
total = coll_links.find({"source":"Pagina12",'parsed':"N"}).count()

for each in coll_links.find({"source":"Pagina12",'parsed':"N"}):

    a_p12 = each['link']
    article_link = "http://"+each['link']

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
                time.sleep(12)
            else:
                break

        page = response.text
        soup = BeautifulSoup(page)

# link.get('title') is not None
        if soup.find('h1').get('text') is not  None:
            article_title = soup.find('h1').text.encode('latin1').decode('utf8')
        else:
            article_title = ''

        if soup.find(class_='volanta').get('text') is not None:
            article_volanta = soup.find(class_='volanta').text
        else:
            article_volanta = ''

        if soup.find(class_='bajada').get('text') is not None:
            article_subtitl = soup.find(class_='bajada').text
        else:
            article_subtitl = ''

        if soup.find(id='cuerpo').get('text') is not None:
            article_body = soup.find(id='cuerpo').text
        else:
            article_body = ''

        #Date Parsing
        date_str = soup.find(class_='fecha')['content'].encode('latin1').decode('utf8')
        date_object = dateparser.parse(date_str)

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
        ok_id = coll_links.update_one({"link":a_p12 },{"$set" : {"parsed":"Y"}})
        print 'Link added:',article_link
    else:
        ok_id = coll_links.update_one({"link":a_p12 },{"$set" : {"parsed":"Y"}})
        print 'Link passed:',article_link

    print "Total Processed:"+str(count)+" of "+str(total)
    count += 1
