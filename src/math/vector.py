import math

#
# A class to help with vectors
# 
class Vector(object):
	# 
	# Init
	# 
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest

	#
	# Rotate the vextor around it's src
	# 
	def rotate(self, angle):
		(x, y) = self.dest
		(x_origin, y_origin) = self.src

		x = float(x)
		y = float(y)
		x_origin = float(x_origin)
		y_origin = float(y_origin)

		angle = angle * (math.pi / 180.0)
		s = math.sin(angle)
		c = math.cos(angle)

		dx = x - x_origin
		dy = y - y_origin
		px = c * dx - s * dy + x_origin
		py = s * dx + c * dy + y_origin

		self.dest = (px, py)
		return self.dest