from src.gfx.actor import Actor

#
# A simple bot
#
class Bot(Actor):

	# Init
	def __init__(self, name, colour = 0x000000):
		Actor.__init__(self, name, colour)
	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self, tick):
		Actor.tick(self, tick)