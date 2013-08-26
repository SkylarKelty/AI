#
# Pathfinding class, avoids other objects
#
class Path(object):
	# Create a new Path
	def __init__(self, world, src, dest):
		self.path = []
		self.world = world
		self.maxG = self.world.grid_density - 1
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
		self.world.setBlockColour(best, 0xCCCCCC)

	# Find the best node(s) we can get to from the current cell
	def getBest(self, src):
		x = src[0]
		y = src[1]
		mW = 0
		chosen = None
		for tX in range(x - 1, x + 2):
			if tX < 0 or tX > self.maxG:
				continue

			for tY in range(y - 1, y + 2):
				if tY < 0 or tY > self.maxG:
					continue
				if tY == 0 and tX == 0:
					continue

			w = self.weight(src, (tX, tY))
			if w > mW:
				chosen = (tX, tY)
		return chosen

	# Return the weight of the given node
	def weight(self, src, dest):
		return abs((src[0] + src[1]) - (dest[0] + dest[1]))