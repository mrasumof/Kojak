__author__ = 'martinrasumoff'

people = ['Havelange','Blatter','Leoz','Baez','Kirchner','Menem','AFA',\
          'Cristobal Lopez','Boudou','Lijo','Grondona',\
          'Maximo','Macri','Vido','Anibal','FIFA','Dilma','Lula','Maduro',\
          'Venezuela','Vandenbroele','Oyarbide','enador','iputad','Clarin','Pontaquarto']

from pymongo import MongoClient

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']

counter = 0
total_recs = coll_parsed.find({"counted":"N"}).count()

for each in coll_parsed.find({"counted":"N"}):
    names = []
    article_link = each['link']
    for person in people:
        if person in each['body']:
            names.append(person)
    if len(names) > 0:
        ok_id = coll_parsed.update({'link':article_link},{"$set": {'names':names,'counted': 'Y'}})
    else:
        ok_id = coll_parsed.update({'link':article_link},{"$set": {'counted': 'Y'}})

    counter += 1
    print str(counter)+" of "+str(total_recs)

