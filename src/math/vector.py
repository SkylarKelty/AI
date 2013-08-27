import math

#
# A class to help with vectors
# 
class Vector(object):
	# 
	# Init
	# 
	def __init__(self, (sx, sy), (dx, dy)):
		self.src = (float(sx), float(sy))
		self.dest = (float(dx), float(dy))

	#
	# Rotate the vextor around it's src
	# 
	def rotate(self, angle):
		(x, y) = self.dest
		(x_origin, y_origin) = self.src

		angle = angle * (math.pi / 180.0)
		s = math.sin(angle)
		c = math.cos(angle)

		dx = x - x_origin
		dy = y - y_origin
		px = c * dx - s * dy + x_origin
		py = s * dx + c * dy + y_origin

		self.dest = (px, py)
		return self.dest

	#
	# Returns the length of this line
	# 
	def length(self):
		x = self.src[0] - self.dest[0]
		y = self.src[1] - self.dest[1]
		d = (x*x) + (y*y)
		return math.sqrt(d)

	#
	# Given a world, does this vector intersect anything at its end point?
	#
	def intersects(self, world):
		cell = world.cellAtPixel(self.dest)
		if cell:
			return world.cells[cell]
		return None