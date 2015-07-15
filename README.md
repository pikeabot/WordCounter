# WordCounter

This app uses BeautifulSoup, pyLucene, Flask and Apache2 to obtain, search and display content.

SCRAPER
-------
The scraper dir contains scrapers for Forbes, CNN, Bloomberg, BusinessInsider, the Guardian and Huffington Post. 
The scrapers only search for new articles within the past day.scrapers in scraper/scraperInit are the same as those in the scraper dir except they search for articles beginning from June 1st, 2015.
To run a scraper in either scraper or scraperInit directory, type:

sudo python scrapername.py

Example: sudo python CNNScraper.py

pyLucene
--------
