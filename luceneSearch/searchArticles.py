#!/usr/bin/env python
import sys, os, lucene, re, logging, datetime, operator
import MySQLdb as mdb
from collections import Counter

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.index import IndexReader, Term, Fields, MultiFields, TermsEnum
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version, BytesRef

#rom nltk.tokenize import RegexpTokenizer
from scraper.config import *

INDEX_DIR = "/var/www/html/WordCounter/luceneSearch/IndexFiles.index"


"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
class Freq(object):
    def __init__(self, freq, date):
        self.freq=freq
        self.date=date

def search(queryString, startDateStr, endDateStr, source):
    #logging.basicConfig(level=logging.INFO)
    #logger = logging.getLogger(__name__)
    	try:
		venv = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
   	except:
		"JVM alread running"
	venv = lucene.getVMEnv()
	venv.attachCurrentThread()
	base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    	directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
    	reader = DirectoryReader.open(directory);
   	searcher = IndexSearcher(reader)
    	analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    
   	query = QueryParser(Version.LUCENE_CURRENT, "contents",
                        analyzer).parse(queryString)
    	scoreDocs = searcher.search(query, 50).scoreDocs
    
   	 #print "%s total matching documents." % len(scoreDocs)
    	freqList=[]
    	for scoreDoc in scoreDocs:
        	doc = searcher.doc(scoreDoc.doc)
        	path = doc.get("path")
        	name = doc.get("name")
        	#print 'path:', doc.get("path"), 'name:', doc.get("name")
        	date = getArticleDate(name, startDateStr, endDateStr, source)
        	if date != None:
            		f = open(str('/home/ubuntu/articles/'+name))
            		count = getCounter(f.readlines()[0].lower(), queryString)
            		freqList.append(Freq(count, int(date.strftime("%s")) * 1000))   
    	del searcher
    	freqListSortedByTime = sorted(freqList, key=operator.attrgetter('date'))
    	sortedFreqDict=[]
    	for freqItem in freqListSortedByTime:
        	sortedFreqDict.append({"date": freqItem.date, "freq": freqItem.freq})
   	return sortedFreqDict

def getCounter(txt, queryString):
    return txt.count(queryString)

def getArticleDate(name, startDateStr, endDateStr, source):
    id = name.split(".")[0]
    con = mdb.connect(HOST, USER, PASSWORD, DB)
    cursor = con.cursor()
    if source!='Select Source':
        cursor.execute("SELECT date_created FROM article where id=%s AND source=%s", (id, source))
        date = cursor.fetchone()
        if date==None:
            return 
    else:
        cursor.execute("SELECT date_created FROM article where id=%s", [id]) 
        date = cursor.fetchone()
    date=date[0]
    if startDateStr!="":
        if date < convertStartStrToDate(startDateStr):
            return 
    if endDateStr!="":
        if date > convertEndStrToDate(endDateStr):
            return 
    return date

def convertStartStrToDate(dateStr):
    dateArray = dateStr.split('-')
    dataIntArray=[]
    for d in dateArray:
        dataIntArray.append(int(d))
    return datetime.datetime(dataIntArray[0], dataIntArray[1], dataIntArray[2], 0, 0,0 )

def convertEndStrToDate(dateStr):
    dateArray = dateStr.split('-')
    dataIntArray=[]
    for d in dateArray:
        dataIntArray.append(int(d))
    return datetime.datetime(dataIntArray[0], dataIntArray[1], dataIntArray[2],23, 59,59 )
