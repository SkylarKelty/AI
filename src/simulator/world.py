from PyQt4 import QtCore, QtGui
from src.gfx.grid import Grid

class World(QtGui.QFrame):
	# Should we render the grid?
	show_grid = True
	# How dense is the world grid?
	grid_density = 10
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

	# Setup the world
	def setup(self, window):
		self.objects = []
		self.window = window

		if World.show_grid:
			self.grid()

	# Run the sim
	def run(self):
		self.timer = QtCore.QBasicTimer()
		self.timer.start(World.tick_rate, self)

	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.tick()
		else:
			QtGui.QFrame.timerEvent(self, event)

	# Show a grid
	def grid(self):
		self.objects.append(Grid(World.grid_density))