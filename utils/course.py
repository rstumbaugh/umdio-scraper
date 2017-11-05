import re
import sys

def flush():
	sys.stdout.flush()

class Course:
	def __init__(self, json):
		self.id = json['course_id']
		self.name = json['name']
		self.credits = json['credits']
		self.semesters = [json['semester']]
		# self.gen_ed = json['gen_ed'] UMD.io has not updated gen ed parsing
		self.core = json['core']
		self.dept_id = json['dept_id']
		self.description = json['description']
		self.relationships = json['relationships']
	
	def __str__(self):
		return '{}: {} ({} credits)'.format(self.id, self.name, self.credits)

def get_courses(semesters):
	api_root = 'http://api.umd.io/v0/courses'

	def get_url(semester, page):
		return '{}?semester={}&page={}&per_page=100'.format(api_root, semester, page)

	courses = {}
	for semester in semesters:
		page = 1
		url = get_url(semester, page)
		response = requests.get(url)

		current_dept = 'AASP'
		while int(response.status_code) != 500:
			print('grabbing courses for {} ({})'.format(current_dept, semester))
			flush()
			json = response.json()
			for course in json:
				course_object = Course(course)
				if course['course_id'] in courses:
					courses.semesters.append(course_object.semester)
				else:
					courses[course['course_id']] = course_object
				if course['dept_id'] != current_dept:
					current_dept = course['dept_id']
			page += 1
			url = get_url(semester, page)
			response = requests.get(url)
	
	return courses
