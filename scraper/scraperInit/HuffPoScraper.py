import os
import datetime
import re
import sys
import pytz
import urllib2
from os import listdir
from os.path import isfile, join
from datetime import date
from scraperutil import *

def getMainURLs(soup):
	#find links
	allLinks=soup.find_all("a", class_="raw_feed")
	links=[]
	for link in allLinks:
		if 'index.xml' in link['href']:
			links.append(link['href'])

	return links

def getGuid(soup):
	#find links
	allLinks=soup.find_all("guid")
	links=[]
	for link in allLinks:
		links.append(link.get_text())

	return links

def getArticleJSON(soup):
	#soup=soupify(url)
	text = str(soup.find("script", type="application/ld+json"))
	text = text.replace('<script type=\"application/ld+json\">', '')
	text = text.replace('</script>', '')
	return json.loads(text, strict = False)

def getTime(dateStr):
	
	date = dateStr[:-6]
	timeZone = dateStr[-5:]
	sign = dateStr[-6:-5]
	d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
	tz = datetime.datetime.strptime(timeZone, "%H:%M")
	#make date time timestamp
	if sign=="-":
		if d.hour+tz.hour>23:
			dt=datetime.datetime(d.year, d.month, d.day+1, (d.hour+tz.hour)-24, d.minute, d.second)
		else:
			dt=datetime.datetime(d.year, d.month, d.day, d.hour+tz.hour, d.minute, d.second)
	else:
		dt=datetime.datetime(d.year, d.month, d.day, d.hour-tz.hour, d.minute, d.second)
	return dt
	

def main():

	'''
	Use Huffington Post rss feeds to find articles
	'''
	siteUrl = 'http://www.huffingtonpost.com/syndication/'

	mainURLsSoup = soupify(siteUrl)
	urls = getMainURLs(mainURLsSoup)

	for url in urls:
		soup = soupify(url)
		links = getGuid(soup)

		for link in links:
			
			try:
				newSoup = soupify(link)
				jsonText = getArticleJSON(newSoup)
				
				time = getTime(jsonText['datePublished'])
				if not inDb(link) and inDate(datetime.datetime(2015, 6, 1, 0, 0, 0), time):
					text = jsonText['articleBody']
					addToDb(time, text.encode('ascii', 'ignore'), link, 'HP')
			except Exception, e:
				print str(e)	
		
if __name__ == "__main__":
	main()