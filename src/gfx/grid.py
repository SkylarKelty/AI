from PyQt4 import QtGui

class Grid(object):
	def __init__(self, density):
		self.density = density
		self.color = QtGui.QColor(0xADE398)

	def render(self, world):
		painter = QtGui.QPainter(world)
		rect = world.contentsRect()

		painter.setPen(self.color)

		xSpacing = rect.width() / self.density
		ySpacing = rect.height() / self.density

		for x in range(self.density):
			x = (x + 1) * xSpacing
			painter.drawLine(x, 0, x, rect.bottom())

		for y in range(self.density):
			y = (y + 1) * ySpacing
			painter.drawLine(0, y, rect.right(), y)