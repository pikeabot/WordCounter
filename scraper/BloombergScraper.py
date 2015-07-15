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
	allLinks=soup.find_all("article")
	links=[]
	for link in allLinks:
		links.append("http://www.bloomberg.com/"+link.find("a")["href"])
	return links

def getJSONURLs(soup):
	#find links
	scripts=soup.find_all("script")
	script = scripts[-1].get_text()
	urls = script.split(",")
	newUrls=[]
	for url in urls:
		if '"url":"http://www.bloomberg.com/' in url:
			u = url.replace('"url":"', '')
			u=u.replace('"', '')
			newUrls.append(u)
	return newUrls

def getArticleJSON(url, soup):
	#soup=soupify(url)
	text = str(soup.find("script", type="application/ld+json"))
	text = text.replace('<script type=\"application/ld+json\">', '')
	text = text.replace('</script>', '')
	return json.loads(text, strict = False)

def getTime(soup):
	#get date string
	dateArray = soup.find("time", class_="published-at time-based hide-time-based" )
	dateStr = dateArray['datetime']

	date = dateStr[:-5]
	d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
	tz = datetime.datetime.strptime("0400", "%H%M")
	#assume time in EST timezone


	if d.hour+tz.hour>23:
		dt=datetime.datetime(d.year, d.month, d.day+1, (d.hour+tz.hour)-24, d.minute, d.second)
	else:
		dt=datetime.datetime(d.year, d.month, d.day, d.hour+tz.hour, d.minute, d.second)

	return dt

def getArticleText(soup):
	#soup=soupify(url)
	text = soup.find("div", class_="article-body__content")
	text = text.find_all("p" )
	cleanedText = []
	for t in text:
		cleanedText.append(t.get_text())
	#concat paragraphs into one text string
	return ' '.join(cleanedText)

def main():

	#Use Bloomberg main page to find 
	siteUrl = 'http://www.bloomberg.com/'

	soup = soupify(siteUrl)
	HTMLurls = getMainURLs(soup)	#get urls to articles listed in HTML
	JSONurls = getJSONURLs(soup)	#get urls to articles listed in javascript
	urls = HTMLurls + JSONurls

	for link in urls:
		try:
			newSoup = soupify(link)
			
			time = getTime(newSoup)
			if not inDb(link) and inDate(getToday(), time):
				text = getArticleText(newSoup)
				addToDb(time, text.encode('ascii', 'ignore'), link, 'B')
		except Exception, e:
				print str(e)
	
if __name__ == "__main__":
	main()
