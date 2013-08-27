from src.gfx.actor import Actor
from src.ai.pathfinding import Path

#
# A simple bot
#
class Bot(Actor):

	#
	# Init
	# 
	def __init__(self, name, colour = 0x000000):
		Actor.__init__(self, name, colour)
		# Change these
		
		# How many blocks in front can we see?
		self.los = 20
		# Whats our field of view?
		self.fov = 180

		# Ignore these
		self.path = None

	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self, tick):
		if self.path:
			self.path.setSource((self.x, self.y))
			self.path.update()
			node = self.path.next()
			if node:
				self.setPos((node[0], node[1]))
			else:
				self.path = None
				self.moveTo(self.world.randomCell(True))

	#
	# Set a target location that we should move too
	# 
	def moveTo(self, cell):
		self.path = Path(self.world, (self.x, self.y), cell)

	#
	# Render our fov
	#
	def renderFOV(self, world):
		pass

	# Render
	def render(self, world):
		self.renderFOV(world)
		Actor.render(self, world)