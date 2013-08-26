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
				self.cells[o.x][o.y] = None
				o.tick()
				self.cells[o.x][o.y] = o

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
				x.append(None)
			self.cells.append(x)

		if World.show_grid:
			self.grid()

		# Test object
		self.direction = 1
		self.test = Actor()
		self.test.setColour(0xCF29B0)
		self.addActor(self.test, self.findEmptyCell())
		self.addActor(Block(), (12, 0))

	# Is a given cell empty?
	def isEmptyCell(self, x, y):
		return self.cells[x][y] is None

	# Find an empty cell
	def findEmptyCell(self):
		for y in range(World.grid_density):
			for x in range(World.grid_density):
				if self.isEmptyCell(x, y):
					return (x, y)
		return None

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
			self.cells[pos[0]][pos[1]] = actor

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