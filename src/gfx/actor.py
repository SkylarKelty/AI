from PyQt4 import QtGui

class Actor(object):
	# Init
	def __init__(self):
		self.setColour(0x000000)
		self.setPos(0, 0)

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

	# Setup
	def setup(self, world):
		self.grid_density = world.grid_density
		self.maxdist = world.grid_density - 1

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