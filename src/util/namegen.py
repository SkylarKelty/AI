import random

#
# A simple name generator
#
female_names = ["Sarah", "Abby", "Kate", "Caitlin", "Kim", "Allison", "Sky"]
male_names = ["Mark", "Bob", "John", "Sean", "Jake", "Jerry", "Matthew"]

def human(gender):
	if gender is "M":
		return random.choice(male_names)
	return random.choice(female_names)