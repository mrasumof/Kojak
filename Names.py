__author__ = 'martinrasumoff'

from pymongo import MongoClient
from bson.son import SON
from textblob import TextBlob
from dateutil import parser
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut

def pos_maker(x):
    x = x.split()
    x = tagger.uni.tag(x)

    return x

#-*- coding: utf8 -*-

from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
from cPickle import dump,load

def loadtagger(taggerfilename):
    infile = open(taggerfilename,'rb')
    tagger = load(infile); infile.close()
    return tagger

def traintag(corpusname, corpus):
    # Function to save tagger.
    def savetagger(tagfilename,tagger):
        outfile = open(tagfilename, 'wb')
        dump(tagger,outfile,-1); outfile.close()
        return
    # Training UnigramTagger.
    uni_tag = ut(corpus)
    savetagger(corpusname+'_unigram.tagger',uni_tag)
    # Training BigramTagger.
    bi_tag = bt(corpus)
    savetagger(corpusname+'_bigram.tagger',bi_tag)
    print "Tagger trained with",corpusname,"using" +\
                "UnigramTagger and BigramTagger."
    return

# Function to unchunk corpus.
def unchunk(corpus):
    nomwe_corpus = []
    for i in corpus:
        nomwe = " ".join([j[0].replace("_"," ") for j in i])
        nomwe_corpus.append(nomwe.split())
    return nomwe_corpus

class cesstag():
    def __init__(self,mwe=True):
        self.mwe = mwe
        # Train tagger if it's used for the first time.
        try:
            loadtagger('cess_unigram.tagger').tag(['estoy'])
            loadtagger('cess_bigram.tagger').tag(['estoy'])
        except IOError:
            print "*** First-time use of cess tagger ***"
            print "Training tagger ..."
            from nltk.corpus import cess_esp as cess
            cess_sents = cess.tagged_sents()
            traintag('cess',cess_sents)
            # Trains the tagger with no MWE.
            cess_nomwe = unchunk(cess.tagged_sents())
            tagged_cess_nomwe = tag_sent(cess_nomwe)
            traintag('cess_nomwe',tagged_cess_nomwe)
            print
        # Load tagger.
        if self.mwe == True:
            self.uni = loadtagger('cess_unigram.tagger')
            self.bi = loadtagger('cess_bigram.tagger')
        elif self.mwe == False:
            self.uni = loadtagger('cess_nomwe_unigram.tagger')
            self.bi = loadtagger('cess_nomwe_bigram.tagger')

def pos_tag(tokens, mmwe=True):
    tagger = cesstag(mmwe)
    return tagger.uni.tag(tokens)

def batch_pos_tag(sentences, mmwe=True):
    tagger = cesstag(mmwe)
    return tagger.uni.batch_tag(sentences)

client = MongoClient("52.25.140.201",27017)
db = client['ProjectCorruption']
coll_parsed = db['Parsed_Articles']

from_year = '01/01/2014'
to_year = '12/31/2014'
source = 'Clarin'
from_year_d = parser.parse(from_year)
to_year_d = parser.parse(to_year)

text_coll = []
for each in coll_parsed.find({'source': source, 'date': {'$gte':from_year_d}, 'date':{'$lte':to_year_d}}).limit(100):
    vlink = each['link']
    vdate = each['date']
    vtext = each['body']
    text_coll.append([vdate,vtext,vlink])

df_columns = ['date','text','link']
df_coll = pd.DataFrame(text_coll,columns=df_columns)

# Read the corpus into a list,
# each entry in the list is one sentence.
cess_sents = cess.tagged_sents()

# Train the unigram tagger
uni_tag = ut(cess_sents)

total = len(df_coll)
Series_sent = []

for index in range(len(df_coll)):
    print int(index)," of total ",total
    sentences = df_coll['text'][index]
    sentences = sentences.split(".")
    counter = 0
    for sentence in sentences:
        vlink = df_coll['link'][index]
        vsent = sentence
        vline = counter
        counter += 1
        Series_sent.append([vlink,vline,vsent])

df_text = pd.DataFrame(Series_sent, columns=['link','counter','text'])

# create Series to include POS..

tagger = cesstag()


df_text['POS']=df_text.text.apply(pos_maker)

keywords = ['corrupcion','corrupto','corrupta','soborno','cohecho','nepotismo','clientelismo','fraude','coima']

names_identifiers = ['np0000p',None]
complete_names = []
for index1 in range(len(df_text)):
    name = ""
    flag = 0
    for index2 in range(len(df_text['POS'][index1])):
        code = df_text['POS'][index1][index2][1]
        if  (code in names_identifiers):
            a = df_text['POS'][index1][index2][0][0]
            if a.isupper():
                if flag == 1:
                    name = name + " "+ df_text['POS'][index1][index2][0]
                    print name
                    flag = 0
                    complete_names.append(name)
                    name = ""
                else:
                    name = name + " "+ df_text['POS'][index1][index2][0]
                    flag = 1
        else:
            if flag == 1:
                flag = 0
                print name
                complete_names.append(name)
                name = ''

print "hello"