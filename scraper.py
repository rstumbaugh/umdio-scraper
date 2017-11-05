import requests
import datetime
import sys
from bs4 import BeautifulSoup
from os import environ as env
from pymongo import MongoClient
from utils.course import get_courses
from utils.professor import get_professors
from utils.gen_ed import get_gen_eds

client = MongoClient(env.get('DB_URI'))
db = client[env.get('DB_NAME')]

semester_codes = ['01', '05', '08', '12']
current_year = datetime.datetime.now().year

# next year's class schedule uploaded around September
if current_year >= 9:
	current_year += 1

years = range(current_year - 3, current_year + 1)
# semesters = [str(year) + sem for year in years for sem in semester_codes]
semesters = ['201608']

courses = get_courses(semesters)
(courses, professors) = get_professors(courses, semesters)

print('found {} courses'.format(len(courses)))
print('found {} professors'.format(len(professors)))
print('grabbing gen eds...')
sys.stdout.flush()

courses = get_gen_eds(courses)
