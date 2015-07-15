import os
import datetime
import re
import sys
import urllib2
from os import listdir
from os.path import isfile, join
from datetime import date
from scraperutil import *

def getMainURLs(soup):
	#find links
	allLinks=soup.find_all("link", title=True)
	links=[]
	for link in allLinks:
		links.append(link['href'])

	return links

def getGuid(soup):
	#find links
	allLinks=soup.find_all("guid")
	links=[]
	for link in allLinks:
		links.append(link.get_text())

	return links

def getArticleText(soup):
	#soup=soupify(url)
	text = soup.find_all("p", class_="zn-body__paragraph")
	#get rid of READ: etc news links and tags
	cleanedText = []
	for t in text:
		if 'READ' in t:
			text.remove(t)
		else:
			cleanedText.append(t.get_text())
	#concat paragraphs into one text string
	return ' '.join(cleanedText)


def getTime(soup):
	
	dateStr = soup.find("meta", itemprop="dateCreated")['content']
	date = dateStr[:-1]
	return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

def main():

	'''
	Use CNN rss feeds to find articles
	'''
	siteUrl = 'http://www.cnn.com/services/rss/'

	mainURLsSoup = soupify(siteUrl)
	urls = getMainURLs(mainURLsSoup)

	for url in urls:
		soup = soupify(url)
		links = getGuid(soup)
		
		for link in links:
			try: 
				newSoup = soupify(link)
				
				time = getTime(newSoup)
				if not inDb(link) and inDate(getToday(), time):
					text = getArticleText(newSoup)
					addToDb(time, text.encode('ascii', 'ignore'), link, 'CNN')
			except Exception, e:
				print str(e)
	
if __name__ == "__main__":
	main()
