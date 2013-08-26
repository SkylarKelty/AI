import random
from PyQt4 import QtCore, QtGui
from src.gfx.grid import Grid
from src.gfx.actor import Actor
from src.gfx.block import Block

class World(QtGui.QFrame):
	# Should we render the grid?
	show_grid = True
	# How dense is the world grid?
	grid_density = 50
	# How often should we tick per second?
	tick_rate = 60

	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (tick rate)/second
	# 
	def tick(self):
		for o in self.objects:
			if hasattr(o, "tick"):
				self.cells[o.x][o.y].remove(o)
				o.tick()
				if not self.isEmptyCell(o.x, o.y):
					self.collide(o)
				self.cells[o.x][o.y].append(o)

	# --------------------------------
	# You shouldnt need to change anything below this line
	# --------------------------------
	
	# Main Init
	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
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

		# Create a bunch of blocks
		for i in range(30):
			cell = self.randomCell(True)
			if cell:
				block = Block()
				self.addActor(block, cell)

	# Is a given cell empty?
	def isEmptyCell(self, x, y):
		return not self.cells[x][y]

	# Find an empty cell
	def findEmptyCell(self):
		for y in range(World.grid_density):
			for x in range(World.grid_density):
				if self.isEmptyCell(x, y):
					return (x, y)
		return None

	# Returns a random cell address
	def randomCell(self, empty = False):
		if empty:
			if self.findEmptyCell() == None:
				return None
			# Get all the empty cells
			empties = []
			for y in range(World.grid_density):
				for x in range(World.grid_density):
					if self.isEmptyCell(x, y):
						empties.append((x, y))
			return random.choice(empties)
		else:
			# Grab a random cell
			x = random.randint(0, World.grid_density)
			y = random.randint(0, World.grid_density)
			return (x, y)

	# Run the sim
	def run(self):
		self.timer = QtCore.QBasicTimer()
		self.timer.start(1000 / World.tick_rate, self)

	# Show a grid
	def grid(self):
		grid = Grid(World.grid_density)
		self.objects.append(grid)

	# Add an actor
	def addActor(self, actor, pos):
		if pos != None:
			actor.setup(self)
			self.objects.append(actor)
			actor.setPos(pos[0], pos[1])
			self.cells[pos[0]][pos[1]].append(actor)

	# Collide event
	def collide(self, obj):
		for o in self.cells[obj.x][obj.y]:
			o.onCollision(obj)
			obj.onCollision(o)

	# Clean up objects post-tick
	def cleanupWorld(self):
		newObj = []
		for o in self.objects:
			if o and o.alive:
				newObj.append(o)
		self.objects = newObj

	# Our paint event
	def paintEvent(self, event):
		for o in self.objects:
			o.render(self)
				
	# Called by the timer
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.tick()
			self.cleanupWorld()
			self.update()
		else:
			QtGui.QFrame.timerEvent(self, event)