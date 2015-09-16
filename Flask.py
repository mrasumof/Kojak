__author__ = 'martinrasumoff'
import flask
from pymongo import MongoClient
from dateutil import parser
import numpy as np
import pandas as pd
import pickle



client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']
#input = open('data_to_upload.pkl', 'wb')
#pickle.load(df, input)

app = flask.Flask(__name__)
#url_for('static', path='/Users/martinrasumoff/Desktop/metis/kojak/css/master.css')

@app.route('/')
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """

    with open("layout2.html", 'r') as viz_file:
        return viz_file.read()

@app.route("/articles", methods=['POST'])
def articles():

    print flask.request.json
    #print flask.request.json[0]
    print flask.request.json['from_subject']

    from_p = flask.request.json['from_subject']
    to_p = flask.request.json['to_subject']
    from_y = flask.request.json['from_year']
    to_y = flask.request.json['to_year']
    from_s = flask.request.json['from_subject']
    to_s = flask.request.json['to_subject']

#   clarin = request.args.get('clarin')
#   lanac = request.args.get('ln')
#   pag12 = request.args.get('p12')
#   infob = request.args.get('infobae')
#   tiemp = request.args.get('ta')
#   ambit = request.args.get('ambito')
#   perfi = request.args.get('perfil')

    print 'from p:',str(from_p)
    print 'to p:'+str(to_p)
    print 'from y:'+from_y
    print 'to y:'+str(to_y)
    print 'from s:'+str(from_s)
    print 'to s:'+str(to_s)
#   print clarin, lanac, pag12, infob, tiemp, ambit, perfi

    from_year = "01/01/"+str(from_y)
    to_year = "12/31/"+str(to_y)

    date_from = parser.parse(from_year)
    date_to = parser.parse(to_year)
    from_pr = float(from_p)
    to_pr = float(to_p)
    from_su = float(from_s)
    to_su = float(to_s)
#
    print date_from
    print date_to
    print "f",from_su
    print "t",to_su

#    list_sources = []

#    if clarin == 'on':
#        list_sources.append("Clarin")

#    if lanacion:
#        list_sources.append("LaNacion")

#    if infobae:
#        list_sources.append("Infobae")

#    if pagina:
#        list_sources.append("Pagina12")
#
#     if tiempo:
#        list_sources.append("TA")

#    if ambito:
#        list_sources.append("Ambito")

#    if perfil:
#        list_sources.append("Perfil")

#    if local_news_only:
#        list_local = ["Y"]
#    else:
#        list_local = ["Y","N"]



    docs = list(coll_parsed.find({"date": {"$gte": date_from}, "date": {"$lte": date_to},\
                                   "polarity": {"$gte": from_pr}, "polarity": {"$lte": to_pr}},\
                                 {'_id': False}).limit(100))

#                                  "subjectivity": {"$gte": from_su}, "subjectivity": {"$lte": to_su}},\
#
#                                  "polarity": {"$gte": from_p}, "polarity": {"$lte": to_p}},\

#db.getCollection('Parsed_Articles').find({"international":"N",
#                              "polarity": {"$gt":-0.5},
#                              "polarity": {"$lt":0.5},
#                              "subjectivity": {"$gt":0.25},
#                              "subjectivity": {"$lt":0.75},
#                              "source": {"$in":["Clarin","LaNacion","TA","Pagina12"]}},
#                              {'_id': false}).count()
#   print type(docs)
#   with open("data_corrupcion_since2012.pkl", 'r') as picklefile:
#    my_old_data = pickle.load(picklefile)
#    my_old_data2 = my_old_data[0:10]

#   docs = my_old_data2.to_json(orient='records')
#    docs = my_old_data2.to_dict()
#    print type(docs)
#    print param

    return flask.jsonify({'result': docs})

app.run(host='0.0.0.0', port=8000, debug=True)



