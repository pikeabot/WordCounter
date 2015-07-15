import os
import datetime
import re
import sys
import urllib2
import httplib
import httplib2
from os import listdir
from os.path import isfile, join
from datetime import date
from scraperutil import *

def getMainURLs(soup):
	#find links
	mainLinks=soup.find_all("a", class_="top-navigation__action")
	links=[]
	for link in mainLinks:
		if link['href'] not in links:
			if link['href']!='http://www.theguardian.com/uk' or link['href']!='/international':
				links.append(link['href'])

	globalLinks=soup.find_all("a", class_="global-navigation__action")
	for link in globalLinks:
		if link['href'] not in links:
			if link['href']!='http://www.theguardian.com/uk' or link['href']!='/international':
				links.append(link['href'])

	return links

def getSubURLs(soup):
	#find links
	mainLinks=soup.find_all("a", class_="fc-item__link" )
	links=[]
	for link in mainLinks:
		if link['href'] not in links:
			links.append(link['href'])
	return links


def getArticleText(soup):

	text = soup.find("div", class_="content__article-body from-content-api js-article__body")
	articleText = text.find_all("p")
	#get rid of READ: etc news links and tags
	cleanedText = []
	for t in articleText:
		cleanedText.append(t.get_text())
	#concat paragraphs into one text string
	return ' '.join(cleanedText)

def getTime(soup):
	#get date string
	dateArray = soup.find("time", itemprop="datePublished" )
	dateStr = dateArray['datetime']
	date = dateStr[:-5]
	timeZone = dateStr[-4:]
	sign = dateStr[-5:-4]
	d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
	tz = datetime.datetime.strptime(timeZone, "%H%M")
	if sign=="-":
		if d.hour+tz.hour>23:
			dt=datetime.datetime(d.year, d.month, d.day+1, (d.hour+tz.hour)-24, d.minute, d.second)
		else:
			dt=datetime.datetime(d.year, d.month, d.day, d.hour+tz.hour, d.minute, d.second)
	else:
		dt=datetime.datetime(d.year, d.month, d.day, d.hour-tz.hour, d.minute, d.second)
	return dt

def getPage(url):

	soup = soupify(url)
	links = getSubURLs(soup)

	for link in links:
		try:
			newSoup = soupify(link)
		
			time = getTime(newSoup)
			if inDate(getToday(), time)!=True:
				print 'Too early'
				return

			if not inDb(link) and inDate(getToday(), time):
				text = getArticleText(newSoup)
				addToDb(time, text.encode('ascii', 'ignore'), link, 'G')
		except Exception, e:
				print str(e)

def main():

	siteUrl = 'http://www.theguardian.com/uk'

	mainURLsSoup = soupify(siteUrl)
	urls = getMainURLs(mainURLsSoup)

	for url in urls:
		for counter in range(1, 5):
			if counter ==1:
				urlPage = url+'/all'
			else:
				urlPage = url+"?page="+str(counter)
			try:
				h = httplib2.Http()
				resp = h.request(urlPage, 'HEAD')
				if int(resp[0]['status']) >= 400:
					break
				else:
					getPage(urlPage)
			except:
				print '400+ error'
		

if __name__ == "__main__":
	main()