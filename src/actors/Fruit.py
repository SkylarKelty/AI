from Actor import Actor

#
# A Tree object
# Spawns fruit to eat
#
class Fruit(Actor):

	# Init
	def __init__(self, tree):
		Actor.__init__(self, "An apple", 0x147514)
		self.ignoreBlocking = True
		self.lifetime = 0
		self.tree = tree
		self.edible = True
		self.hungerValue = 10
		self.canPass = True

	# 
	# Tick
	# 
	def tick(self, world, tick):
		self.lifetime += 1

		# Go rotten after 50 ticks
		if self.lifetime > 50:
			self.kill()

	#
	# On kill, respawn
	#
	def kill(self):
		self.tree.doIn(15, "replenish", self.cell)
		Actor.kill(self)