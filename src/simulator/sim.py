import sys
from PyQt4 import QtCore, QtGui
from world import World

class Window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setGeometry(0, 0, 800, 800)
		self.setWindowTitle('AI Sim')

	def center(self):
		screen = QtGui.QDesktopWidget().screenGeometry()
		size =  self.geometry()
		x = (screen.width() - size.width()) / 2
		y = (screen.height() - size.height()) / 2
		self.move(x, y)

def main():
	app = QtGui.QApplication(sys.argv)
	w = Window()
	w.center()

	# Setup the world
	world = World()
	world.setup(w)

	# Show the window
	w.show()

	# Run the world
	world.run()

	sys.exit(app.exec_())