import random
from Actor import Actor
from Fruit import Fruit

#
# A Tree object
# Spawns fruit to eat
#
class Tree(Actor):

	# Init
	def __init__(self):
		Actor.__init__(self, "An apple tree", 0x855D00)
		self.ignoreBlocking = True
		self.fruit = {}

	#
	# setPos
	#
	def setPos(self, cell):
		r = Actor.setPos(self, cell)
		# Spawn fruit
		for c in self.world.surroundingCells(cell):
			self.doIn(random.randint(2, 15), "replenish", c)
		return r

	#
	# Spawn fruit
	# 
	def spawn(self, cell):
		if self.world.isEmptyCell(cell):
			f = Fruit(self)
			self.world.addActor(f, cell)
			self.fruit[cell] = f
		else:
			self.doIn(2, "replenish", cell)

	#
	# Called by doIn
	#
	def onAction(self, name, cell):
		if name == "replenish":
			self.spawn(cell)