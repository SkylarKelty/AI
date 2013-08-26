from PyQt4 import QtCore, QtGui
from src.gfx.grid import Grid

class World(QtGui.QFrame):
	# Should we render the grid?
	show_grid = True
	# How dense is the world grid?
	grid_density = 50
	# How often should be tick per second?
	tick_rate = 120

	# 
	# A tick - your main entry point to the world.
	# This should be overridden, and will be called once per (tick rate)/second
	# 
	def tick(self):
		pass

	# --------------------------------
	# You shouldnt need to change anything below this line
	# --------------------------------
	
	# Main Init
	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
		self.objects = []

		if World.show_grid:
			self.grid()

	# Run the sim
	def run(self):
		self.timer = QtCore.QBasicTimer()
		self.timer.start(World.tick_rate, self)

	# Show a grid
	def grid(self):
		grid = Grid(World.grid_density)
		self.objects.append(grid)

	# Clean up objects post-tick
	def cleanupWorld(self):
		newObj = []
		for o in self.objects:
			if o:
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