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
		self.movingToFood = False

		Bot.__init__(self, namegen.human(self.gender), 0xBA6C49)

	#
	# Tick
	#
	def tick(self, world, tick):
		# Randomly spawn a child, with a 1 in a 100 tick chance
		# But only if we arent too hungry
		if self.hunger <= 10 and random.randint(0, 100) == 0:
			self.spawn(world)

		# Die if we are too hungry
		if self.hunger == 30:
			print "%s died of hunger :(" % self
			return self.kill()

		# Increase hunger every 5 ticks
		if tick % 5 == 0:
			self.hunger += 1
			if self.hunger == 10:
				print "%s is hungry!" % self
		
		Bot.tick(self, world, tick)

	#
	# Spawn a child
	#
	def spawn(self, world):
		child = Human()
		world.addActor(child, world.findEmptyCell())
		child.moveTo(world.randomCell(True))

	#
	# What do we do when we spy something?
	# 
	def onSight(self, cell, obj):
		# Search for food if we are hungry
		if hasattr(obj, "edible") and obj.edible:
			if not self.movingToFood and self.hunger > 10:
				print "%s has found food!" % self
				self.movingToFood = True
				self.moveTo(cell)

	#
	# Called when we collide with something
	# 
	def onCollision(self, obj):
		# If we are hungry, eat it
		if self.hunger > 10 and hasattr(obj, "edible") and obj.edible:
			obj.kill()
			self.hunger -= obj.hungerValue
			print "%s ate %s" % (self, obj)

	#
	# What do when we finish our path?
	# 
	def onPathFinish(self):
		self.movingToFood = False
		self.moveTo(self.world.randomCell(True))