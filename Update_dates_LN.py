__author__ = 'martinrasumoff'
import pymongo
from pymongo import MongoClient
from datetime import datetime
import requests
from bs4 import BeautifulSoup

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']

coll_parsed = db['Parsed_Articles']

print coll_parsed
from datetime import datetime

def convert_date(a):
#    print type(a)
    b = a.split('\n')
    time1 = False
    for each in b:
        c = each.strip()
        if 'CalcularTimestamp(' in each:
            if c[0] != '*':
                if c[0:3] == 'var':
                    d = each.split(",")
                    time1 = datetime.fromtimestamp(float(d[1]))
                    return time1
    return time1

changed = 0

total_recs = coll_parsed.find({"source":"Clarin","parsed":"N"}).count()

for each in coll_parsed.find({"source":"Clarin", "parsed":"N"}):
    article_link = each['link']
    response = requests.get(article_link)
    page = response.text
    soup = BeautifulSoup(page)
    try:
        a = soup.find_all(class_="breadcrumb")[0].find(type='text/javascript').text
    except IndexError:
        continue
    else:
        article_date = convert_date(a)
        if article_date != False:
            ok_id = coll_parsed.update_one({"link":article_link},{"$set" : {"date":article_date, \
                                                                            "parsed":"Y"}})
    changed +=1
    print "Processed: "+str(changed)+" of "+str(total_recs)+" - "+article_link