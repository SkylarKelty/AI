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
		self.firstTick = True
		self.fruit = {}

	# 
	# Tick
	# 
	def tick(self, world, tick):
		# Grab surrounding cells if first tick
		if self.firstTick:
			self.surroundingCells = []
			for cell in world.surroundingCells(self.cell):
				if world.isEmptyCell(cell):
					self.surroundingCells.append(cell)

			# Spawn fruit
			for cell in self.surroundingCells:
				self.doIn(random.randint(2, 15), "replenish", [cell])

			self.firstTick = False
			return

		# Parent tick
		Actor.tick(self, world, tick)

	#
	# Spawn fruit
	# 
	def spawn(self, cell):
		if self.world.isEmptyCell(cell):
			f = Fruit(self)
			self.world.addActor(f, cell)
			self.fruit[cell] = f

	#
	# Called by doIn
	#
	def onAction(self, name, args):
		if name == "replenish":
			self.spawn(args[0])