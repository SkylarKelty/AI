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
		# Create a bunch of blocks
		for i in range(30):
			cell = self.randomCell(True)
			if cell:
				self.addActor(Block(), cell)

		# Create an actor
		barry = Bot("Barry")
		self.addActor(barry, self.findEmptyCell())
		barry.moveTo(self.randomCell(True))


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

		# Setup our cell array
		self.cells = []
		for x in range(World.grid_density):
			x = []
			for y in range(World.grid_density):
				x.append([])
			self.cells.append(x)

		if World.show_grid:
			self.grid()

		# Setup
		self.setup()

	# 
	# A preTick will be called once per (tick rate)/second
	# 
	def preTick(self, tick):
		for o in self.objects:
			self.cells[o.x][o.y].remove(o)
			o.tick(tick)
			if not self.isEmptyCell((o.x, o.y)):
				self.collide(o)
			self.cells[o.x][o.y].append(o)

	#
	# Is a given cell empty?
	# 
	def isEmptyCell(self, (x, y)):
		return not self.cells[x][y]

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
			actor.setPos((pos[0], pos[1]))
			self.cells[pos[0]][pos[1]].append(actor)

	#
	# Set the colour of a cell
	#
	def setBlockColour(self, (x, y), colour):
		blk = Block(colour)
		blk.setup(self)
		blk.setPos((x, y))
		self.renderables.append(blk)

	#
	# Collide event
	#
	def collide(self, obj):
		for o in self.cells[obj.x][obj.y]:
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