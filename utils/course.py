import re
import requests
from bs4 import BeautifulSoup

class Course:
	def __init__(self, id):
		self.id = id
		self.semesters = []
	
	def __str__(self):
		return '{}: {} ({} credits)'.format(self.id, self.name, self.credits)

def parse_course(text):
	course = Course(text['id'])
	course.name = text.find('span', class_='course-title').text.strip()
	course.credits = text.find(class_='course-min-credits').text.strip()
	
	approved_texts = text.find_all(class_='approved-course-text')
	other_text = text.find(class_='course-text')

	if (len(approved_texts) > 0):
		body = ''.join([div.text for div in approved_texts]) + str(other_text)
	else:
		body = str(other_text)

	print('{}: {}'.format(text['id'], body))

	return course

def get_courses(semesters):
	# get URLs for each semester & department
	department_urls = ['https://ntst.umd.edu/soc/201608/CMSC']
	# for semester in semesters:
	# 	print('getting departments for {}'.format(semester))
	# 	response = requests.get('https://ntst.umd.edu/soc/{}/'.format(semester))
	# 	soup = BeautifulSoup(response.text, 'html.parser')
	# 	depts = soup.find_all('span', class_='prefix-abbrev')

	# 	for dept in depts:
	# 		department_urls.append('https://ntst.umd.edu/soc/{}/{}'.format(semester, dept.text))

	# get courses from each URL
	courses = {}
	
	for url in department_urls[:1]:
		match = re.match(r'https://ntst\.umd\.edu/soc/(\d{6})/([A-Z]{4})', url)
		(semester, dept_id) = match.groups()
		print('scraping courses for {} ({})'.format(dept_id, semester))
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

	return courses
