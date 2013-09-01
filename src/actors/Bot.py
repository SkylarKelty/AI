import math
from PyQt4 import QtGui
from Actor import Actor
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
		
		# How many blocks in front can we see?
		self.los = 5
		# Whats our field of view?
		self.fov = 120

		# Ignore these
		self.path = None
		self.direction = (1, 0)
		self.FOVLines = []

	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self, world, tick):
		# Move first
		if self.path:
			node = self.path.next()
			if node:
				self.setPos((node[0], node[1]))
			else:
				self.path = None
				self.onPathFinish()

		# Check LOS
		insight = self.getFOV(world)
		if insight:
			for cell in insight:
				for obj in insight[cell]:
					self.onSight(cell, obj)

	#
	# What do we do when we spy something?
	# 
	def onSight(self, cell, obj):
		pass

	#
	# What do when we finish our path?
	# 
	def onPathFinish(self):
		pass

	# -----------------------------------------------------
	# You shouldnt need to change anything below this line
	# -----------------------------------------------------

	#
	# Set a target location that we should move too
	# 
	def moveTo(self, cell):
		self.path = Path(self.world, self, (self.x, self.y), cell)

	#
	# Override: Calculate direction as well
	# 
	def setPos(self, cell):
		(x, y) = self.cell
		Actor.setPos(self, cell)
		# If we have moved, update the direction
		if self.x != x or self.y != y:
			self.direction = (self.constrain(self.x - x, -1, 1), self.constrain(self.y - y, -1, 1))

	#
	# Detect objects in our fov
	#
	def getFOV(self, world):
		self.FOVLines = []
		rect = world.contentsRect()
		cellHeight = rect.height() / self.grid_density

		# Origin
		(x1, y1) = (self.trueX(rect, self.x), self.trueY(rect, self.y))
		angle = self.getRotation()

		sight = {}
		fovhits = {}
		for l in range(self.los):
			(x2, y2) = (x1, (y1 - self.trueY(rect, l)) - (cellHeight / 2)) # Base

			# Draw fan
			for i in range(-(self.fov / 2), (self.fov / 2) + 1, 5):
				if i in fovhits:
					continue

				vec = Vector((x1, y1), (x2, y2))
				(rx, ry) = vec.rotate(angle + i)
				cell = world.cellAtPixel((rx, ry))
				if not cell in sight:
					sight[cell] = []
				intersection = vec.intersects(world)
				if intersection:
					fovhits[i] = intersection
					sight[cell] = intersection
				else:
					self.FOVLines.append((x1, y1, rx, ry))
		return sight

	#
	# Render our fov
	#
	def renderFOV(self, world):
		painter = QtGui.QPainter(world)
		painter.setPen(QtGui.QColor(0x00CC00))
		for (x1, y1, rx, ry) in self.FOVLines:
			painter.drawLine(x1, y1, rx, ry)

	#
	# Returns our angle
	# 
	def getRotation(self):
		dirmap = {
			(0, -1): 0,
			(1, -1): 45,
			(1, 0): 90,
			(1, 1): 135,
			(0, 1): 180,
			(-1, 1): 225,
			(-1, 0): 270,
			(-1, -1): 315
		}
		if self.direction in dirmap:
			return dirmap[self.direction]
		return 0

	def trueX(self, rect, x):
		sizeX = rect.width() / self.grid_density
		return (x * sizeX) + (sizeX / 2)

	def trueY(self, rect, y):
		sizeY = rect.height() / self.grid_density
		return (y * sizeY) + (sizeY / 2)

	# Render
	def render(self, world):
		if world.debugMode:
			self.renderFOV(world)
		Actor.render(self, world)