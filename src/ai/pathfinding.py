#
# Pathfinding class
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

	# Update the path
	def update(self):
		pass

	# Returns the next node on the path
	def next(self):
		if self.path:
			return self.path[0]
		return None

	# Returns the entire path
	def path(self):
		return self.path