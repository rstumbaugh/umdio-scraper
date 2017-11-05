import requests
import datetime
from bs4 import BeautifulSoup
from os import environ as env
from pymongo import MongoClient
from utils.course import get_courses

client = MongoClient(env.get('DB_URI'))
db = client[env.get('DB_NAME')]

semester_codes = ['01', '05', '08', '12']
current_year = datetime.datetime.now().year

# next year's class schedule uploaded around September
if current_year >= 9:
	current_year += 1

years = range(current_year - 3, current_year + 1)
semesters = [str(year) + sem for year in years for sem in semester_codes]

courses = get_courses(semesters)
for course_id, course in courses.items():
	print(course)