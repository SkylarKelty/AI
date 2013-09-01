from Actor import Actor

#
# A simple blocking object
#
class Block(Actor):

	# Init
	def __init__(self, colour = 0x333333):
		Actor.__init__(self, "A Block", colour)
		self.ignoreBlocking = True
	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self, world, tick):
		pass # Do nothing