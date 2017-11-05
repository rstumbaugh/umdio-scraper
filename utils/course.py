
class Course:
	def __init__(self, id):
		self.id = id
		self.semesters = []

def parse_course(text):
	return Course(text['id'])