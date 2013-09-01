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
		self.hunger = 0
		self.tiredness = 0
		self.gender = random.choice(["F", "M"])

		Bot.__init__(self, namegen.human(self.gender), 0xBA6C49)

	#
	# Tick
	#
	def tick(self, world, tick):
		# Randomly spawn a child, with a 1 in a 100 tick chance
		if random.randint(0, 100) == 0:
			self.spawn(world)

		# Die if we are too hungry
		if self.hunger == 15:
			return self.kill()

		# Increase hunger every 5 ticks
		if tick % 5 == 0:
			self.hunger += 1
		
		Bot.tick(self, world, tick)

	#
	# Spawn a child
	#
	def spawn(self, world):
		child = Human()
		world.addActor(child, world.findEmptyCell())
		child.moveTo(world.randomCell(True))