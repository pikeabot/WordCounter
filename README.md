# WordCounter

This app uses BeautifulSoup, pyLucene, MySQL, Flask and Apache2 to obtain, search and display content.

SCRAPER
-------
The scraper dir contains scrapers for Forbes, CNN, Bloomberg, BusinessInsider, the Guardian and Huffington Post. 
The scrapers only search for new articles within the past day.scrapers in scraper/scraperInit are the same as those in the scraper dir except they search for articles beginning from June 1st, 2015.

The scrapers stores the article timestamp, source and source url in MySQL and the source text in a directory called articles. The MySQL schema is here:
https://github.com/pikeabot/WordCounter/blob/master/scraper/schema.sql

To run a scraper in either scraper or scraperInit directory, type:

sudo python scrapername.py

Example: sudo python CNNScraper.py

pyLucene
--------
http://lucene.apache.org/pylucene/
pyLucene is used to index and search the text files. To manually index the article text files, cd into the luceneSearch directory and run:
sudo python indexFiles.py ~/articles
