

def insert_courses(db, courses):
	collection = db.courses
	collection.delete_many({})
	courses_as_dicts = [course.as_dict() for course in courses.values()]
	result = collection.insert_many(courses_as_dicts)
	print('{} course records inserted'.format(len(result.inserted_ids)))

def insert_professors(db, professors):
	print('inserting profs...')

def insert_departments(db, departments):
	collection = db.departments
	collection.delete_many({})
	result = collection.insert_many(departments)
	print('{} department records inserted'.format(len(result.inserted_ids)))