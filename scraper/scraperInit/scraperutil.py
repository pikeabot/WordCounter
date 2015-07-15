import os
import datetime
import json
import re
import MySQLdb as mdb
import sys
import urllib2
from datetime import date
from bs4 import BeautifulSoup
from config import *

def inDb(link):
	con = mdb.connect(HOST, USER, PASSWORD, DB)
	cursor = con.cursor()
	if cursor.execute("SELECT * FROM article where source_url=%s", [link]):
		return True
	else:
		return False

'''
scrape HTML using BeautifulSoup
'''
def soupify(url):
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()

	return BeautifulSoup(page)

def inDate(earliestDate, currentDate):
	if currentDate>earliestDate:
		return True
	else:
		return False

def addToDb(date_created, text, link, source):
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		cursor = con.cursor()
		cursor.execute("INSERT INTO article (date_created, source_url, source) \
			VALUES (%s, %s, %s)", (date_created, link, source))
		con.commit()
		id=cursor.lastrowid
		fileName='/home/ubuntu/articles/'+str(id)+'.txt'
		f=open(fileName, 'w')
		f.write(text)
		f.close()
	except mdb.Error, e:
	  
	    print "Error %d: %s" % (e.args[0], e.args[1])
	    #sys.exit(1)

	finally:
	    
	    if con:
	        con.close()



def getToday():
	d = datetime.datetime.now()
	return datetime.datetime(d.year, d.month, d.day, 0, 0, 0)
