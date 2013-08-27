import random

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
		path = []
		self.exclusions = {}
		last = src
		while last and last[0] != self.destination[0] or last[1] != self.destination[1]:
			new = self.getBest(last)
			if new == last or not new:
				break
			path.append(new)
			self.exclusions[new] = True
			last = new
		return path

	# Find the best node(s) we can get to from the current cell
	def getBest(self, src):
		x = src[0]
		y = src[1]
		mW = -1

		# Choose our best option
		chosen = None
		options = []
		for tX in range(x - 1, x + 2):
			if tX < 0 or tX > self.maxG:
				continue

			for tY in range(y - 1, y + 2):
				if tY < 0 or tY > self.maxG:
					continue
				if tY == 0 and tX == 0:
					continue

				# Ignore this if we are blocked or in exclusions
				if not self.world.isEmptyCell((tX, tY)) or (tX, tY) in self.exclusions:
					continue

				options.append((tX, tY))

				w = self.weight((tX, tY), self.destination)
				if mW == -1 or w < mW:
					chosen = (tX, tY)
					mW = w

		# Choose something random if we failed
		if not chosen and len(options) > 0:
			# Go through every cell thats not in the exclusions list
			chosen = random.choice(options)

		# Finished!
		return chosen

	# Return the weight of the given node
	def weight(self, src, dest):
		xWeight = abs(src[0] - dest[0])
		yWeight = abs(src[1] - dest[1])
		return xWeight + yWeight