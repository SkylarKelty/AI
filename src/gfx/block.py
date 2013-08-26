from actor import Actor

#
# A simple blocking object
#
class Block(Actor):

	# Init
	def __init__(self):
		Actor.__init__(self, 0x855D00, "A Block")
	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self):
		pass # Do nothing