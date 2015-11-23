__author__ = 'martinrasumoff'

from pymongo import MongoClient
from bson.son import SON
from textblob import TextBlob
from dateutil import parser
import pymongo
import pandas as pd
import matplotlib.pyplot as plt



client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']

from_year = '01/01/2014'
to_year = '12/31/2014'
from_year_d = parser.parse(from_year)
to_year_d = parser.parse(to_year)

df_columns = ['date','text']

text_coll = []
for each in coll_parsed.find({'source':'LaNacion', 'date': {'$gte':from_year_d}, 'date':{'$lte':to_year_d}}):
    vdate = each['date']
    vtext = each['body']
    text_coll.append([vdate,vtext])

df_coll = pd.DataFrame(text_coll,columns=df_columns)

from nltk.corpus import stopwords

stop = stopwords.words('spanish')
stop += ['.',',','(',')',"'",'"']

df_coll['clean_body'] = df_coll['body'].apply(lambda x: [item for item in x if item not in stop])

print "hello"
