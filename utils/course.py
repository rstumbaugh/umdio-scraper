import re
import requests
import sys

class Course:
	def __init__(self, json):
		self.course_id = json['course_id']
		self.name = json['name']
		self.credits = json['credits']
		self.semesters = [json['semester']]
		self.gen_ed = []
		self.core = json['core']
		self.dept_id = json['dept_id']
		self.dept_name = json['department']
		self.description = str(json['description'])
		self.relationships = json['relationships']
		self.professors = []

	def as_dict(self):
		return self.__dict__

def get_semester_name(code):
  year = code[:4]
  month = code[4:]
  if month == '08':
    month = 'Fall'
  elif month == '12':
    month = 'Winter'
  elif month == '01':
    month = 'Spring'
  elif month == '05':
    month = 'Summer'

  return '{} {}'.format(month, year)

def get_courses(semesters):
	'''
		Takes array of semester codes and returns dict
		of {course_id: Course object}
	'''
	
	api_root = 'http://api.umd.io/v0/courses'

	def get_url(semester, page):
		return '{}?semester={}&page={}&per_page=100'.format(api_root, semester, page)

	courses = {}
	for semester in semesters:
		print('grabbing courses for ' + semester)
		sys.stdout.flush()

		page = 1
		url = get_url(semester, page)
		response = requests.get(url)
		while int(response.status_code) not in [500, 404]:
			json = response.json()
			for course in json:
				if course['course_id'] in courses:
					courses[course['course_id']].semesters.append(semester)
				else:
					courses[course['course_id']] = Course(course)

			page += 1
			url = get_url(semester, page)
			response = requests.get(url)
	
	return courses
