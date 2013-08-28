import random
from PyQt4 import QtCore, QtGui
from src.gfx.grid import Grid
from src.actors.Bot import Bot
from src.gfx.block import Block

class World(QtGui.QFrame):
	# Should we render the grid?
	show_grid = True
	# How dense is the world grid?
	grid_density = 50
	# How often should we tick per second?
	tick_rate = 10

	# 
	# A tick will be called once per (tick rate)/second
	# 
	def tick(self, tick):
		pass

	# 
	# Setup- your first entry point to the world.
	# 
	def setup(self):
		# Create an actor
		barry = Bot("Barry")
		self.addActor(barry, self.findEmptyCell())
		barry.moveTo(self.randomCell(True))

		# Create a bunch of blocks
		for i in range(50):
			cell = self.randomCell(True)
			if cell:
				self.addActor(Block(), cell)


	# --------------------------------
	# You shouldnt need to change anything below this line
	# --------------------------------
	
	#
	# Main Init
	#
	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
		self.renderables = []
		self.objects = []
		self.cells = {}
		self.cell_colours = {}
		for x in range(World.grid_density):
			for y in range(World.grid_density):
				self.cells[(x, y)] = []
				self.cell_colours[(x, y)] = []

		if World.show_grid:
			self.grid()

		# Setup
		self.setup()

	# 
	# A preTick will be called once per (tick rate)/second
	# 
	def preTick(self, tick):
		for o in self.objects:
			self.cells[(o.x, o.y)].remove(o)
			o.tick(tick)
			if not self.isEmptyCell((o.x, o.y)):
				self.collide(o)
			self.cells[(o.x, o.y)].append(o)

	#
	# Is a given cell empty?
	# 
	def isEmptyCell(self, cell):
		return not self.cells[cell]

	#
	# Find an empty cell
	# This is a more efficient version of randomCell(True)
	#
	def findEmptyCell(self):
		for y in range(World.grid_density):
			for x in range(World.grid_density):
				if self.isEmptyCell((x, y)):
					return (x, y)
		return None

	#
	# Returns a random cell address that is, optionally, empty
	#
	def randomCell(self, empty = False):
		if empty:
			if self.findEmptyCell() == None:
				return None
			# Get all the empty cells
			empties = []
			for y in range(World.grid_density):
				for x in range(World.grid_density):
					if self.isEmptyCell((x, y)):
						empties.append((x, y))
			return random.choice(empties)
		else:
			# Grab a random cell
			x = random.randint(0, World.grid_density)
			y = random.randint(0, World.grid_density)
			return (x, y)

	#
	# Returns true if a cell exists at the given coords
	#
	def cellExists(self, cell):
		return cell in self.cells

	#
	# Returns the cell at a set of pixel coords
	#
	def cellAtPixel(self, cell):
		if cell in self.cells:
			return self.cells[cell]

		(x, y) = cell
		rect = self.contentsRect()
		sizeX = rect.width() / self.grid_density
		sizeY = rect.height() / self.grid_density

		minX = int((x - (x % sizeX)) / sizeX)
		minY = int((y - (y % sizeY)) / sizeY)
		if (minX, minY) in self.cells:
			return (minX, minY)

		return None

	#
	# Returns all the valid cells around the current one
	#
	def surroundingCells(self, (x, y)):
		options = []
		for tX in range(x - 1, x + 2):
			for tY in range(y - 1, y + 2):
				if not self.cellExists((tX, tY)) or (tY == 0 and tX == 0):
					continue
				options.append((tX, tY))
		return options

	#
	# Run the sim
	#
	def run(self):
		self.ticks = 0
		self.timer = QtCore.QBasicTimer()
		self.timer.start(1000 / World.tick_rate, self)

	#
	# Show a grid
	#
	def grid(self):
		grid = Grid(World.grid_density)
		self.renderables.append(grid)

	#
	# Add an actor
	#
	def addActor(self, actor, pos):
		if pos != None:
			actor.setup(self)
			self.objects.append(actor)
			actor.setPos(pos)
			self.cells[pos].append(actor)

	#
	# Set the colour of a cell
	#
	def setBlockColour(self, cell, colour = 0x000000, permanent = True):
		if not self.cellExists(cell):
			return

		blk = Block(colour)
		blk.setup(self)
		blk.setPos(cell)

		# Clear out the current block
		if self.cell_colours[cell]:
			o = self.cell_colours[cell]
			if o in self.renderables:
				self.renderables.remove(o)
			if o in self.cell_colours[cell]:
				self.cell_colours[cell].remove(o)

		self.cell_colours[cell].append(blk)

		# Add to render queue?
		if permanent:
			self.renderables.append(blk)
		else:
			blk.render(self)

	#
	# Collide event
	#
	def collide(self, obj):
		for o in self.cells[(obj.x, obj.y)]:
			o.onCollision(obj)
			obj.onCollision(o)

	#
	# Clean up objects post-tick
	#
	def cleanupWorld(self):
		newObj = []
		for o in self.objects:
			if o and o.alive:
				newObj.append(o)
		self.objects = newObj

	#
	# Our paint event
	#
	def paintEvent(self, event):
		for o in self.renderables:
			o.render(self)
		for o in self.objects:
			o.render(self)
	
	#
	# Called by the timer
	#
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.preTick(self.ticks)
			self.tick(self.ticks)
			self.cleanupWorld()
			self.update()
			self.ticks = self.ticks + 1
		else:
			QtGui.QFrame.timerEvent(self, event)