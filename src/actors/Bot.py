from PyQt4 import QtGui
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
		self.los = 5
		# Whats our field of view?
		self.fov = 180

		# Ignore these
		self.path = None
		self.direction = (1, 0)

	#
	# Calculate direction
	# 
	def setPos(self, cell):
		(x, y) = self.cell
		Actor.setPos(self, cell)
		# If we have moved, update the direction
		if self.x != x or self.y != y:
			self.direction = (self.x - x, self.y - y)

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
		painter = QtGui.QPainter(world)
		rect = world.contentsRect()
		painter.setPen(QtGui.QColor(0x00CC00))

		(dx, dy) = self.direction
		(x, y) = self.cell
		for i in range(self.los):
			x += dx
			y += dy

			# Break if the cell doesnt exist
			if not world.cellExists((x, y)):
				continue

			# If this cell has a blocking object on it, break this los
			actors = world.cells[(x, y)]
			result = False
			for actor in actors:
				if actor.losBlocking:
					result = True
					break
			if result:
				break

			# Set the colour to show its in our LOS
			painter.drawLine(self.trueX(rect, self.x), self.trueY(rect, self.y), self.trueX(rect, x), self.trueY(rect, y))

	def trueX(self, rect, x):
		sizeX = rect.width() / self.grid_density
		return (x * sizeX) + (sizeX / 2)

	def trueY(self, rect, y):
		sizeY = rect.height() / self.grid_density
		return (y * sizeY) + (sizeY / 2)

	# Render
	def render(self, world):
		self.renderFOV(world)
		Actor.render(self, world)