from PyQt4 import QtGui

class Actor(object):

	# Init
	def __init__(self, name, colour = 0x000000):
		self.name = name
		self.setColour(colour)
		self.setSpeed(1)
		self.cell = (0, 0)
		self.x = 0
		self.y = 0

		# Can this actor go through other actors?
		self.ignoreBlocking = False

	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self, tick):
		pass


	# --------------------------------
	# You shouldnt need to change anything below this line
	# --------------------------------

	# Setup
	def setup(self, world):
		self.world = world
		self.grid_density = world.grid_density
		self.maxdist = world.grid_density - 1
		self.direction = 1
		self.alive = True

	# Set our colour
	def setColour(self, colour):
		self.colour = QtGui.QColor(colour)

	# Set our speed (how many blocks can we move per second?)
	def setSpeed(self, speed):
		self.speed = speed

	# Set our position
	def setPos(self, (x, y)):
		e = False
		if x > self.maxdist:
			x = self.maxdist
			e = True

		if x < 0:
			x = 0
			e = True

		if y > self.maxdist:
			y = self.maxdist
			e = True

		if y < 0:
			y = 0
			e = True

		if self.world.isEmptyCell((x, y)) or self.ignoreBlocking:
			self.x = x
			self.y = y
			self.cell = (x, y)
			return not e

		return False

	# Called when we collide with something
	def onCollision(self, obj):
		print "%s collided with %s!" % (self.name, obj.name)

	# Move right
	def moveRight(self):
		return self.setPos((self.x + 1, self.y))

	# Move left
	def moveLeft(self):
		return self.setPos((self.x - 1, self.y))

	# Move up
	def moveUp(self):
		return self.setPos((self.x, self.y - 1))

	# Move down
	def moveDown(self):
		return self.setPos((self.x, self.y + 1))

	# Render
	def render(self, world):
		painter = QtGui.QPainter(world)
		rect = world.contentsRect()

		painter.setPen(self.colour)

		# Render equal to one grid size
		sizeX = rect.width() / self.grid_density
		sizeY = rect.height() / self.grid_density

		# Pad in
		x = self.x * sizeX
		y = self.y * sizeY

		# Draw
		painter.fillRect(x + 1, y + 1, sizeX - 2, sizeY - 2, self.colour)

	# Delete this Actor
	def kill(self):
		self.alive = False

	# Our string
	def __toString(self):
		return self.name