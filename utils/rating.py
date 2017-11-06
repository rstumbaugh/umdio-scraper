import json
import firebase_admin
from firebase_admin import credentials
import os
from os import environ as env

credentials_file = 'tmp_credentials.json'

def prep_credentials():
	props = [
		'type', 'project_id', 'private_key_id', 'private_key', 
		'client_email', 'client_id', 'auth_uri', 'token_uri',
		'auth_provider_x509_cert_url', 'client_x509_cert_url'
	]

	firebase_credentials = {prop: env.get(prop.upper()) for prop in props}
	
	with open(credentials_file, 'w') as f:
		f.write(json.dumps(firebase_credentials))
	print('wrote credentials to ' + credentials_file)

def cleanup_credentials():
	os.remove(credentials_file)
	print('cleaned up credentials')

def link_ratings(courses):
	'''
		Adds average ratings & rating count to each course in courses
	'''
	cred = credentials.Certificate(credentials_file)
	firebase_admin.initialize_app(cred)

