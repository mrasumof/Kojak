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

    print flask.request.json['from_year']
    print flask.request.json['to_year']
    print flask.request.json['checked_sources']

    from_y = flask.request.json['from_year']
    to_y = flask.request.json['to_year']
    list_sources = flask.request.json['checked_sources']

    print 'from y:'+from_y
    print 'to y:'+str(to_y)

    from_year = "01/01/"+str(from_y)
    to_year = "12/31/"+str(to_y)

    date_from = parser.parse(from_year)
    date_to = parser.parse(to_year)

    print date_from
    print date_to

    docs = list(coll_parsed.find({"date": {"$gte": date_from, "$lte": date_to},\
                                  "source": {"$in": list_sources}},\
                                 {'_id': False}).limit(300))

    print list_sources

    return flask.jsonify({'result': docs})

app.run(host='0.0.0.0', port=8000, debug=True)