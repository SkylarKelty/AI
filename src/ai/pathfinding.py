#
# Pathfinding class
#
class Path(object):
	# Create a new Path
	def __init__(self, world):
		self.world = world

	# Set the starting location of the path
	def setSource(self, cell):
		pass

	# Set the finishing location of the path
	def setDestination(self, cell):
		pass

	# Update the path
	def update(self):
		pass

	# Returns the next node on the path
	def next(self):
		pass

	# Returns the entire path
	def path(self):
		pass