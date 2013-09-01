import random

#
# Pathfinding class, avoids other objects
#
class Path(object):
	# Create a new Path
	def __init__(self, world, actor, src, dest):
		self.path = []
		self.actor = actor
		self.world = world
		self.maxG = self.world.grid_density - 1
		self.setSource(src)
		self.setDestination(dest)
		self.exclusions = {}
		self.last = None
		self.calculatePath()

	# Set the starting location of the path
	def setSource(self, cell):
		self.source = cell

	# Set the finishing location of the path
	def setDestination(self, cell):
		self.destination = cell

	# Returns the next node on the path
	def next(self):
		if len(self.path) > 0:
			return self.path.pop(0)
		return None

	# Returns the entire path
	def path(self):
		return self.path

	# Find a full path from the supplied cell
	def calculatePath(self):
		self.path = []
		self.exclusions = {}
		last = self.source
		while last != self.destination and len(self.path) <= self.world.grid_density:
			new = self.getBest(last)
			if new == last or not new:
				break
			self.path.append(new)
			self.exclusions[new] = True
			last = new

	# Find the best node(s) we can get to from the current cell
	def getBest(self, src):
		x = src[0]
		y = src[1]
		mW = -1

		# Choose our best option
		chosen = None
		options = self.world.surroundingCells(src)
		for cell in options:
			# Ignore this if we are blocked or in exclusions
			if not self.actor.canCollide(cell) or cell in self.exclusions:
				options.remove(cell)
				continue

			w = self.weight(cell, self.destination)
			if mW == -1 or w < mW:
				chosen = cell
				mW = w

		# Choose something random if we failed
		if not chosen and len(options) > 0:
			# Go through every cell thats not in the exclusions list
			chosen = random.choice(options)

		self.exclusions[chosen] = True

		# Finished!
		return chosen

	# Return the weight of the given node
	def weight(self, src, dest):
		xWeight = abs(src[0] - dest[0])
		yWeight = abs(src[1] - dest[1])
		return xWeight + yWeight