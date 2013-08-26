import sys
from PyQt4 import QtCore, QtGui

class Window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setGeometry(300, 300, 300, 300)
		self.setWindowTitle('AI Sim')

def main():
	app = QtGui.QApplication(sys.argv)
	w = Window()
	w.show()
	sys.exit(app.exec_())