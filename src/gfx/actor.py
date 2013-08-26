from PyQt4 import QtGui

class Actor(object):
	# Init
	def __init__(self):
		self.setColour(0x000000)
		self.setPos(0, 0)

	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (World.tick rate)/second
	# 
	def tick(self):
		if self.direction == 1:
			if not self.moveRight():
				self.direction = 2
				return
		if self.direction == 2:
			if not self.moveDown():
				self.direction = 3
				return
		if self.direction == 3:
			if not self.moveLeft():
				self.direction = 4
				return
		if self.direction == 4:
			if not self.moveUp():
				self.direction = 1
				return

	# Set our colour
	def setColour(self, colour):
		self.colour = QtGui.QColor(colour)

	# Set our position
	def setPos(self, x, y):
		self.x = x
		self.y = y

	# Move right
	def moveRight(self):
		self.x = self.x + 1
		if self.x > self.maxdist:
			self.x = self.maxdist
			return False
		return True

	# Move left
	def moveLeft(self):
		self.x = self.x - 1
		if self.x < 0:
			self.x = 0
			return False
		return True

	# Move up
	def moveUp(self):
		self.y = self.y - 1
		if self.y < 0:
			self.y = 0
			return False
		return True

	# Move down
	def moveDown(self):
		self.y = self.y + 1
		if self.y > self.maxdist:
			self.y = self.maxdist
			return False
		return True

	# Setup
	def setup(self, world):
		self.world = world
		self.grid_density = world.grid_density
		self.maxdist = world.grid_density - 1
		self.direction = 1
		self.alive = True

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