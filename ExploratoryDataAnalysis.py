__author__ = 'martinrasumoff'
import pymongo
from pymongo import MongoClient
import pandas as pd

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']

total_recs = coll_parsed.find().count()
count = 0
for each in coll_parsed.find():
    article_link = each['link']
    t_keywords = each['conf_interes']+each['corrupcion']+each['soborno']+each['compr_votos']+each['cohecho']+each['nepotismo']+\
        each['clientelismo']+each['fraude']+each['enriq_ilicito']+each['coima']+each['corrupta']+each['corrupto']

    coll_parsed.update({"link":article_link},{"$set":{"tot_keywords":t_keywords}})
    count += 1
    print "Processed: "+str(count)+" of "+str(total_recs)
