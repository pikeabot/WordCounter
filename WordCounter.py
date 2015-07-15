#!/usr/bin/env python
import sys, os, lucene, thread, json
from java.io import File
from flask import Flask, render_template, url_for, request
from flask import g, Markup, jsonify
from flaskext.mysql import MySQL
from luceneSearch.searchArticles import search
from scraper.config import *

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = USER
app.config['MYSQL_DATABASE_PASSWORD'] = PASSWORD
app.config['MYSQL_DATABASE_DB'] = DB
app.config['MYSQL_DATABASE_HOST'] = HOST

mysql.init_app(app)

#cursor = mysql.get_db().cursor()


#main app
@app.route('/', methods=['GET', 'POST'])
def index ():

	if request.method == 'POST':
		#if request.form['submit'] == 'talk':
		searchStr = request.form.get('searchString')
		source = request.form['source']
		startDateStr = request.form['searchStartDate']
		endDateStr = request.form['searchEndDate']
		freqList=search(searchStr, startDateStr, endDateStr, source)
		if source == 'Select Source':
			source='All'
		if endDateStr == '':
			endDateStr = 'All'
		if startDateStr == '':
			startDateStr='All'
		return render_template('index.html', queryString = searchStr, \
											startDate = startDateStr, \
											endDate = endDateStr, \
											source = source, \
											searchResult=json.dumps(freqList))
	else:
		return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)
