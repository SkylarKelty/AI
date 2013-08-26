#
# Pathfinding class, avoids other objects
#
class Path(object):
	# Create a new Path
	def __init__(self, world, src, dest):
		self.path = []
		self.world = world
		self.setSource(src)
		self.setDestination(dest)
		self.update()

	# Set the starting location of the path
	def setSource(self, cell):
		self.source = cell

	# Set the finishing location of the path
	def setDestination(self, cell):
		self.destination = cell

	# Returns the next node on the path
	def next(self):
		if self.path:
			return self.path[0]
		return None

	# Returns the entire path
	def path(self):
		return self.path

	# Update the path
	def update(self):
		self.path = self.getPath(self.source)

	# Find a path from the supplied cell
	def getPath(self, src):
		best = self.getBest(src)

	# Find the best node(s) we can get to from the current cell
	def getBest(self, src):
		x = src[0]
		y = src[1]

		for tX in range(x - 1, x + 1):
			print tX

			for tY in range(y - 1, y + 1):
				print tY

	# Return the weight of the given node
	def weight(self, src, dest):
		return abs((src[0] + src[1]) - (dest[0] + dest[1]))