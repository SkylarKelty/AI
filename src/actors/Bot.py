import math
from PyQt4 import QtGui
from src.gfx.actor import Actor
from src.ai.pathfinding import Path
from src.math.vector import Vector

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
		self.fov = 90

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
			self.direction = (self.constrain(self.x - x, -1, 1), self.constrain(self.y - y, -1, 1))

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

		# Origin
		(x1, y1) = (self.trueX(rect, self.x), self.trueY(rect, self.y))
		angle = self.getRotation()

		(x2, y2) = (x1, y1 - self.trueY(rect, self.los)) # Base
		
		# Center point
		vec = Vector((x1, y1), (x2, y2))
		(x2, y2) = vec.rotate(angle)
		painter.drawLine(x1, y1, x2, y2)

		# Left point
		(x2, y2) = vec.rotate(-(self.fov / 2))
		painter.drawLine(x1, y1, x2, y2)

		# right point
		(x2, y2) = vec.rotate(self.fov)
		painter.drawLine(x1, y1, x2, y2)

	#
	# Constrains a number to a min/max
	# 
	def constrain(self, x, xmin, xmax):
		if x > xmax:
			return xmax
		if x < xmin:
			return xmin
		return x

	#
	# Returns our angle
	# 
	def getRotation(self):
		if self.direction == (0, -1):
			return 0
		if self.direction == (1, -1):
			return 45
		if self.direction == (1, 0):
			return 90
		if self.direction == (1, 1):
			return 135
		if self.direction == (0, 1):
			return 180
		if self.direction == (-1, 1):
			return 225
		if self.direction == (-1, 0):
			return 270
		if self.direction == (-1, -1):
			return 315
		return 0

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