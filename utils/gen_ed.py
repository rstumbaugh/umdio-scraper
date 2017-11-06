import re
import sys
import requests
from bs4 import BeautifulSoup

def extract_gen_eds(text):
	newline_regex = re.compile(r'[\t\r\n]')
	text = text.strip().split(':')[1]
	text = newline_regex.sub('', text)
	text = text.replace('(', ' (').replace(')', ') ')
	text = text.replace('or', ' or ')
	text = text.replace('  ', ' ')

	return [code.strip() for code in text.split(',')]

def get_gen_eds(courses):
	''' 
		Takes dict of {course_id, Course object} & parses gen eds 
		UMD.io's Gen Ed parsing is still not perfect, can be improved
	'''

	checked_depts = []
	semesters_depts = {(course.semesters[-1], course.dept_id) for course in courses.values()}
	for semester, dept_id in semesters_depts:
		if dept_id in checked_depts:
			continue
		else:
			checked_depts.append(dept_id)
		print('checking gen eds for {} ({})'.format(dept_id, semester))
		sys.stdout.flush()

		url = 'https://ntst.umd.edu/soc/{}/{}'.format(semester, dept_id)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')

		for course_div in soup.find_all('div', class_='course'):
			if course_div['id'] not in courses:
				print('**** not found in umd.io: {} ({}) ****'.format(course_div['id'], semester))
				continue

			gen_ed_block = course_div.find(class_='gen-ed-codes-group')
			if gen_ed_block and len(gen_ed_block.text.strip()) > 0:
				gen_ed = extract_gen_eds(gen_ed_block.text)
			else:
				gen_ed = []

			course_id = course_div['id']
			courses[course_id].gen_ed = gen_ed

	return courses