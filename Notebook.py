__author__ = 'martinrasumoff'
import pymongo
from pymongo import MongoClient
import pandas as pd
import dateparser

def find_words(body_txt,keyword):
    count_wrd = 0
    for each_word in body_txt.split():
        if each_word == keyword:
            count_wrd += 1

    return count_wrd

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']

coll_parsed = db['Parsed_Articles']

print coll_parsed

no_dates = []
count = 0
total_rec = coll_parsed.find({"parsed":"N"}).count()

for each_doc in coll_parsed.find({"parsed":"N"}):

    article_link = each_doc['link']

    a = each_doc['body']
    date_art = each_doc['date']
    titl_art = each_doc['title']

    kywrd_0 = find_words(a,"corrupcion") + find_words(a,u'corrupci\xf3n')
    kywrd_1 = find_words(a,'corrupto') + find_words(a,'corruptos')
    kywrd_2 = find_words(a,'corrupta') + find_words(a,'corruptas')
    kywrd_3 = find_words(a,'cohecho') + find_words(a,'cohechos') + find_words(a,'"cohecho"')
    kywrd_4 = find_words(a,'soborno') + find_words(a,'sobornos')
    kywrd_5 = find_words(a,'coima') + find_words(a,'coimas')
    kywrd_6 = find_words(a,'enriquecimiento ilicito') + find_words(a,'enriquecimientos ilicitos')
    kywrd_7 = find_words(a,'conflicto de interes') + find_words(a,'conflictos de interes')
    kywrd_8 = find_words(a,'nepotismo')
    kywrd_9 = find_words(a,'fraude') + find_words(a,'fraude')
    kywrd_10 = find_words(a,'compra de votos') + find_words(a,'compras de votos')
    kywrd_11 = find_words(a,'clientelismo')
    tot_words = len(a)

    if ((date_art == None)):
        no_dates.append(article_link)

    coll_parsed.update({"link":article_link},{"$set":{"corrupcion":kywrd_0,\
                                                      "corrupto":kywrd_1,\
                                                      "corrupta":kywrd_2,\
                                                      "cohecho":kywrd_3,\
                                                      "soborno":kywrd_4,\
                                                      "coima":kywrd_5,\
                                                      "enriq_ilicito":kywrd_6,\
                                                      "conf_interes":kywrd_7,\
                                                      "nepotismo":kywrd_8,\
                                                      "fraude":kywrd_9,\
                                                      "compr_votos":kywrd_10,\
                                                      "clientelismo":kywrd_11,\
                                                      "total_wrds":tot_words,\
                                                      "parsed":"Y"
                                                     }})
    count +=1
    print "Source:"+each_doc['source']+" Analyzed: "+str(count)+" of "+str(total_rec)

for each in no_dates:
    print "No Date:",each




