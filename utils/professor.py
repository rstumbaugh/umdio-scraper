import re
import sys
import requests

class Professor:
	def __init__(self, name):
		self.name = name
		self.courses = []
	
	def __str__(self):
		return '{}: {}'.format(self.name, self.courses)

def check_professor_name(name):
	if name == 'Niwaer Ai' or name == 'Anwar Mamat':
		return 'Anwar Mamat (Niwaer Ai)'
	if name == 'Thomas Reinhart':
		return 'Thomas Reinhardt'
	if re.search(r'TBA', name):
		return ''

def get_professors(courses, semesters):
	'''
		Gets professors for each course in each semester
		Upates course objects
	'''

	def get_url(semester, page):
		url = 'http://api.umd.io/v0/professors?per_page=100&semester={}&page={}'
		return url.format(semester, page)

	professors = {}
	for semester in semesters:
		print('grabbing professors for ' + semester)
		sys.stdout.flush()

		page = 1
		url = get_url(semester, page)
		response = requests.get(url)
		while response.status_code != 500:
			json = response.json()
			for professor_json in json:
				prof = check_professor_name(professor_json['name'])
				course_ids = professor_json['courses']
				if len(prof) == 0:
					continue

				if prof not in professors:
					professors[prof] = Professor(professor_json)

				# for each course, add professor to course and add course to professor
				for course_id in course_ids:
					courses[course_id].professors.append(prof)
					if course_id not in professors[prof].courses:
						professors[prof].courses.append(course_id)

			page += 1
			url = get_url(semester, page)
			response = requests.get(url)

	return (courses, professors)
