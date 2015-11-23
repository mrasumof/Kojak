__author__ = 'martinrasumoff'
import flask
from pymongo import MongoClient
from dateutil import parser

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']

from_y = 2015
to_y = 2015

from_year = "01/01/"+str(from_y)
to_year = "12/31/"+str(to_y)

date_from = parser.parse(from_year)
date_to = parser.parse(to_year)

docs = list(coll_parsed.find({"date": {"$gte": date_from, "$lte": date_to}},\
                                 {'_id': False}).limit(100))

print "hello"