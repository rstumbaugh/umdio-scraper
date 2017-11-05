import requests
import datetime
from bs4 import BeautifulSoup
from os import environ as env
from pymongo import MongoClient
from utils.course import parse_course

client = MongoClient(env.get('DB_URI'))
db = client[env.get('DB_NAME')]

semester_codes = ['01', '05', '08', '12']
current_year = datetime.datetime.now().year

# next year's class schedule uploaded around September
if current_year >= 9:
	current_year += 1

years = range(current_year - 3, current_year + 1)
semesters = [str(year) + sem for year in years for sem in semester_codes]

# get URLs for each semester & department
department_urls = []
for semester in semesters:
	response = requests.get('https://ntst.umd.edu/soc/{}/'.format(semester))
	soup = BeautifulSoup(response.text, 'html.parser')
	depts = soup.find_all('span', class_='prefix-abbrev')

	for dept in depts:
		department_urls.append('https://ntst.umd.edu/soc/{}/{}'.format(semester, dept.text))

# get courses from each URL
courses = {}
for url in department_urls:
	print('checking ' + url)
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')

	course_data = soup.find_all('div', class_='course')
	course_objects = [parse_course(course) for course in course_data]

	# if course already found, update 'semesters'; otherwise, add it as a new course
	for course in course_objects:
		if course.id in courses:
			courses[course.id].semesters.append(course.semester)
		else:
			courses[course.id] = course


print(courses)