from PyQt4 import QtGui

class Actor(object):

	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self, world, tick):
		pass

	# Called when we collide with something
	def onCollision(self, obj):
		print "%s collided with %s!" % (self.name, obj.name)

	# -----------------------------------------------------
	# You shouldnt need to change anything below this line
	# -----------------------------------------------------

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

		# Does this actor block the LOS of other actors?
		self.losBlocking = True

	# Setup
	def setup(self, world):
		self.world = world
		self.grid_density = world.grid_density
		self.maxdist = world.grid_density - 1
		self.alive = True

	# Set our colour
	def setColour(self, colour):
		self.colour = QtGui.QColor(colour)

	# Set our speed (how many blocks can we move per second?)
	def setSpeed(self, speed):
		self.speed = speed

	# Set our position, ensuring its in the grid
	def setPos(self, (x, y)):
		constrained_x = self.constrain(x, 0, self.maxdist)
		constrained_y = self.constrain(y, 0, self.maxdist)

		if self.world.isEmptyCell((constrained_x, constrained_y)) or self.ignoreBlocking:
			self.x = constrained_x
			self.y = constrained_y
			self.cell = (constrained_x, constrained_y)
			return not (constrained_x != x or constrained_y != y)

		return False

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

	#
	# Constrains a number to a min/max
	# 
	def constrain(self, x, xmin, xmax):
		if x > xmax:
			return xmax
		if x < xmin:
			return xmin
		return x

	# Delete this Actor
	def kill(self):
		self.alive = False

	# Our string
	def __str__( self ):
		return self.name