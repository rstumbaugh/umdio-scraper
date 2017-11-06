import json
import firebase_admin
from firebase_admin import credentials, db
import os
import sys
from os import environ as env

if env.get('ENVIRONMENT') == 'dev':
	credentials_path = 'creds/dev.json'
else:
	credentials_path = 'creds/prod.json'

def link_ratings(courses, professors):
	'''
		Adds average ratings & rating count to each course in courses
	'''
	print('linking course ratings...')
	sys.stdout.flush()

	cred = credentials.Certificate(credentials_path)
	app = firebase_admin.initialize_app(
		cred, 
		options={ 'databaseURL': env.get('FIREBASE_DB_URL') }
	)
	
	response = db.reference('/courses').get()
	for course, obj in response.items():
		if course not in courses or 'avgDiff' not in obj:
			continue
		
		courses[course].avg_diff = obj['avgDiff']
		courses[course].avg_int = obj['avgInt']
		courses[course].num_responses = len(obj['ratings'])
		
	return courses