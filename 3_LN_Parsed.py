__author__ = 'martinrasumoff'

import pymongo
from pymongo import MongoClient
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
import time
from dateutil import parser

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']

coll_articles = db['Articles']
coll_links = db['Links_to_articles']
coll_parsed = db['Parsed_Articles']

print coll_links
print coll_articles
print coll_parsed

count = 1
total = coll_links.find({"source":"Clarin",'parsed':"N"}).count()

#b.inventory.find( { $and: [ { price: { $ne: 1.99 } }, { price: { $exists: true } } ] } )
for each in coll_links.find({"source":"Clarin",'parsed':"N"}):

    article_link = each['link']

    # Only adding the article if it is not existent currently
    exist = coll_parsed.find_one({"link": article_link})
    if exist == None:

        print "Gathering:"+each['link']

        response = requests.get(article_link)
        while response.status_code != 200:
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

        if "edant" in article_link:
            edition = "old"
        else:
            edition = "new"

        if soup.find('tu1') != None:
            article_title = soup.find('tu1').text
        else:
            if edition == "new":
                if soup.find('h1') != None:
                    article_title = soup.find('h1').text
                else:
                    article_title = ''
            else:
                article_title = ''

        if soup.find(class_='ea01') != None:
            article_volanta = soup.find(class_='ea01').text
        else:
            if edition == "new":
                if soup.find(class_='volanta') != None:
                    article_volanta = soup.find(class_='volanta').text
                else:
                    article_volanta = ''
            else:
                article_volanta = ''

        if soup.find(class_='e05') != None:
            article_subtitl = soup.find(class_='e05').text
        else:
            if edition == "new":
                if soup.find('i') != None:
                    article_subtitl = soup.find('i').text
                else:
                    article_subtitl = ''
            else:
                article_subtitl = ''

        if soup.find(class_='e07') != None:
                article_body = soup.find(class_='e07').text
        else:
            if edition == "new":
                if soup.find(class_="nota") != None:
                    article_body = soup.find(class_="nota").text
                else:
                    article_body = ''
            else:
                article_body = ''

        if soup.find(class_='e33') != None:
                article_date_txt = soup.find(class_='e33').text
        else:
            if edition == "new":
                article_date_txt = ''
            else:
                article_date_txt = ''

        #article_date = dateparser.parse(soup.find(class_='fecha').text.encode('latin1').decode('utf8'))
        # Parsing date
        if edition == "old":
            date = soup.find_all(class_='e33')[2]['href']
            year = date[8:12]
            month = date[13:15]
            day = date[16:18]
            date_str = year+"/"+month+"/"+day
            article_date = parser.parse(date_str)
        else:
            article_date = parser.parse('01/01/1980')

        article_source = 'Clarin'

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
        print 'Link passed:',article_link

    print "Total Processed:"+str(count)+" of "+str(total)
    count += 1
