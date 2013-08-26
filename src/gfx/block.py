from actor import Actor

#
# A simple blocking object
#
class Block(Actor):

	# Init
	def __init__(self, colour = 0x855D00):
		Actor.__init__(self, "A Block", colour)
	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self):
		pass # Do nothing