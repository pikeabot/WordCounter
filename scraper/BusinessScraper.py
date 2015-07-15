import os
import datetime
import re
import sys
import urllib2
import httplib2
from os import listdir
from os.path import isfile, join
from datetime import date
from scraperutil import *

def getURLs(soup):
	#find links
	mainLinks=soup.find_all("a", class_="title")
	links=[]
	for link in mainLinks:
		links.append(link['href'])

	span8Links = soup.find_all("div", class_="span8 river-post")
	for span8 in span8Links:
		links.append(span8.find("a")['href'])
	
	span4Links = soup.find_all("div", class_="span4 river-image")
	for span4 in span4Links:
		links.append(span4.find("a")['href'])

	return links

def getArticleText(soup):

	text = soup.find_all("p")
	#get rid of READ: etc news links and tags
	cleanedText = []
	for t in text:
		cleanedText.append(t.get_text())
	#concat paragraphs into one text string
	return ' '.join(cleanedText)

def getTime(soup):
	jsonDate = soup.find("script", type="application/ld+json" ).get_text()
	jsonDate = jsonDate.replace("//<![CDATA[", "")
	jsonDate = jsonDate.replace("//]]>", "")
	jsonDate = jsonDate.strip()

	jDate = json.loads(jsonDate, strict = False)
	dateCreated = jDate['dateCreated']
	dateCreated = dateCreated[:-1]
	d = datetime.datetime.strptime(dateCreated, "%Y-%m-%dT%H:%M:%S")
	return datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second)


def getPage(urls):

	for link in urls:
		try:
			newSoup = soupify(link)
		
			time = getTime(newSoup)
			if inDate(datetime.datetime(getToday()), time)!=True:
				print 'Too early'
				return

			if not inDb(link) and inDate(datetime.datetime(2015, 4, 20, 0, 0, 0), time):
				text = getArticleText(newSoup)
				addToDb(time, text.encode('ascii', 'ignore'), link)
				#print link

		except:
			print link

def main():

	siteUrl = 'http://www.businessinsider.com/'

	#taken from 'All' section of businessinsider.com
	
	for counter in range(1, 20):

		if counter > 1 :
			urlPage = siteUrl+"?page="+str(counter)
		else:
			urlPage = siteUrl

		h = httplib2.Http()
		resp = h.request(urlPage, 'HEAD')
		if int(resp[0]['status']) >= 400:
			break
		else:
			urlsSoup = soupify(urlPage)	#get all links on page
			urls = getURLs(urlsSoup)
			for link in urls:
				try:
					newSoup = soupify(link)
				
					time = getTime(newSoup)
					if inDate(getToday(), time)!=True:
						print 'Too early'
						break

					if not inDb(link) and inDate(getToday(), time):
					
						text = getArticleText(newSoup)
						addToDb(time, text.encode('ascii', 'ignore'), link, 'BI')
						#print link
				except Exception, e:
					print str(e)

	
if __name__ == "__main__":
	main()