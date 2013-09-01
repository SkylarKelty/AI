import random
from src.util import namegen
from Bot import Bot

#
# A simple human
#
class Human(Bot):

	#
	# Init
	# 
	def __init__(self):
		self.gender = random.choice(["F", "M"])
		Bot.__init__(self, namegen.human(self.gender), 0xBA6C49)