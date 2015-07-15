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
	mainLinks=soup.find_all("td", style="font-weight:bold;")
	links=[]
	for link in mainLinks:
		links.append(link.a['href'])
	subLinks=soup.find_all("td", style="padding-left:10px;")
	for link in subLinks:
		links.append(link.a['href'])
	
	return links

def getGuid(soup):
	#find links
	link = soup.find("guid")
	return link.get_text()

def getItems(soup):
	#soup=soupify(url)
	items = soup.find_all("item")
	return items


def getTime(soup):
	#get date string
	dateArray = soup.find(itemprop="datePublished")
	da1=str(dateArray).split("=")
	da2 = da1[1].split(" ")
	dateStr = da2[0]
	dateStr = dateStr.replace('"', '')
	#get Year-Month-Day-Hour:Minute:Second
	date = dateStr[:-6]
	#get the time zone in the form of UTC+/-XX00
	timeZone = dateStr[-5:]
	#get if time zone is +/-
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

def getAllText(soup):
	#soup=soupify(url)
	
	text = getArticleText(soup)
	pages = getPageCount(soup)
	if pages!=None:
		for i in range(0, pages-1):
			nextTextLink = soup.find("li", class_="next_page")
			nextUrl = nextTextLink.find("a")
			nextSoup = soupify(nextUrl['href'])

			nextText = getArticleText(nextSoup)
			text = text+nextText
	return text
	
def getPageCount(soup):
	pages = soup.find("li", class_="page_count")
	return len(pages.find_all("b"))
	

def getArticleText(soup):
	#soup=soupify(url)
	text = soup.find("div", class_="body_inner")
	text = text.find_all("p")

	cleanedText = []
	for t in text:
		cleanedText.append(t.get_text())
	#concat paragraphs into one text string
	return ' '.join(cleanedText)


def main():

	'''
	Use Forbes rss feeds to find articles
	'''
	siteUrl = 'http://www.forbes.com/fdc/rss.html'

	mainURLsSoup = soupify(siteUrl)
	urls = getMainURLs(mainURLsSoup)

	for url in urls:
		soup = soupify(url)
		items = getItems(soup)
		for item in items:

			try:
				link = getGuid(item)
				newSoup = soupify(link)
				
				time = getTime(newSoup)
				if not inDb(link) and inDate(getToday(), time):
					text = getArticleText(newSoup)
					addToDb(time, text.encode('ascii', 'ignore'), link, 'F')

			except Exception, e:
				print str(e)
	
if __name__ == "__main__":
	main()
