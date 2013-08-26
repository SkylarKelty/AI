class Grid(object):
	def __init__(self, density):
		self.density = density

	def render(self, world):
		for x in range(self.density):
			for y in range(self.density):
				pass