import requests
import datetime
import sys
from bs4 import BeautifulSoup
from os import environ as env
from pymongo import MongoClient
from utils.course import get_courses, get_semester_name
from utils.professor import get_professors
from utils.gen_ed import get_gen_eds
from utils.db import insert_courses, insert_professors, insert_departments, insert_semesters
from utils.rating import link_ratings

client = MongoClient(env.get('DB_URI'))
db = client[env.get('DB_NAME')]

semester_codes = ['01', '05', '08', '12']
current_year = datetime.datetime.now().year

# next year's class schedule uploaded around September
if current_year >= 9:
	current_year += 1

years = range(current_year - 3, current_year + 1)
semesters = [str(year) + sem for year in years for sem in semester_codes]

# get courses and professors for all semesters
courses = get_courses(semesters)
(courses, professors) = get_professors(courses, semesters)

print('found {} courses'.format(len(courses)))
print('found {} professors'.format(len(professors)))
print('grabbing gen eds...')
sys.stdout.flush()

# link gen eds for all courses (umd.io gen ed parsing not great)
courses = get_gen_eds(courses)

# link ratings to all courses
link_ratings(courses, '')

# insert courses & departments into DB
unique_depts = {(course.dept_id, course.dept_name) for course in courses.values()}
depts = [{'dept_id': dept_id, 'department': name} for (dept_id, name) in unique_depts]

unique_semesters = {semester for course in courses.values() for semester in course.semesters}
semesters = [{'semester_code': code, 'semester_name': get_semester_name(code)} for code in unique_semesters]

insert_courses(db, courses)
insert_departments(db, depts)
insert_semesters(db, semesters)
