__author__ = 'martinrasumoff'

from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import requests
import time
import pymongo
from pymongo import MongoClient

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
print db
collection = db['Links_to_articles']
print collection

starting_point = 0

keyword = 'corrupcion'

#url_1 = 'http://www.pagina12.com.ar/buscador/resultado.php?q='

#url = url_1+keyword

url = 'http://www.pagina12.com.ar/buscador/resultado.php?qid=cb002895b7780bb0aa5db812b4919b4d.0'
response = requests.get(url)

#Setting the starting point
starting_point = 0

site_page = 1
total_added = 0

#while ((response.status_code == 200)):
    page = response.text
    soup = BeautifulSoup(page)

    print "Page:",site_page

    flag = 0

    a = []
    for link in soup.find_all('a'):
        try:
            link['title']
        except:
            pass
        else:
            if link['title'] == 'Ir a la nota':
                a.append(link)

    for link in a:

        article_link = "www.pagina12.com.ar"+link
        article_source = "P12"

        # Only adding the link if it is not existent currently
        exist = collection.find_one({"link": article_link})
        if exist == None:
            article_object = {"link":article_link, "source":article_source}
            #article_id = collection.insert_one(article_object)
            total_added += 1
            print 'Link added:',article_link
            print 'Total added:',str(total_added)
        else:
            print 'Link passed:',article_link

#    url = "http://buscar.lanacion.com.ar/clientelismo?sort=default&offSet="+str(10*site_page)
#    site_page += 1

#    while True:

#        try:
#            response = requests.get(url)
#        except ConnectionError:
#            print "Oopss...we've been cut off... :( Let's take some time off :)"

#        if response.status_code != 200:
#            print "Sleeping..."
#            time.sleep(12)
#        else:
#            break

print 'Grand Total added:',str(total_added)
