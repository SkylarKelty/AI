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
		self.direction = (1, 0)
		painter = QtGui.QPainter(world)
		rect = world.contentsRect()
		painter.setPen(QtGui.QColor(0x00CC00))
		plane = self.getPlane(rect)

		# Origin
		(x1, y1) = (self.trueX(rect, self.x), self.trueY(rect, self.y))
		(dx, dy) = self.direction
		#(cx, cy) = self.cell
		angle = self.getRotation()

		#for i in range(self.los):
		#	cx += dx
		#	cy += dy

		(x2, y2) = (x1, y1 - self.trueY(rect, self.los)) # Base x2, y2
		

		vec = Vector((x1, y1), (x2, y2))
		(x2, y2) = vec.rotate(angle)
		painter.drawLine(x1, y1, x2, y2)

		# Left point
		(x2, y2) = vec.rotate(-(self.fov / 2))
		painter.drawLine(x1, y1, x2, y2)

		# right point
		(x2, y2) = vec.rotate(self.fov)
		painter.drawLine(x1, y1, x2, y2)

		# Draw plane
		#x3 = (x2 - (plane / 2)) * (math.cos(angle) * -math.sin(angle))
		#y3 = y2 * (math.sin(angle) * -math.cos(angle))
		#painter.drawLine(x2, y2, x3, y3)

		#x3 = x2 + (plane / 2)
		#y3 = y2
		#painter.drawLine(x2, y2, x3, y3)



		return

		(dx, dy) = self.direction
		(x, y) = self.cell
		for angle in range(-(self.fov / 2), (self.fov / 2) + 1):
			angle_multiply = 1.0 / float(angle)
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
				
				(x2, y2) = (self.trueX(rect, x), self.trueY(rect, y))
				painter.drawLine(x1, y1, x2, y2)

	#
	# Returns the size of our plane
	# 
	def getPlane(self, rect):
		sizeX = rect.width() / self.grid_density
		side = self.los * sizeX
		angle = self.fov / 2.0
		radius = math.sqrt((math.pow(side, 2) * 2) - ((2 * (side*side)) * math.cos(angle)))
		return radius * 2

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