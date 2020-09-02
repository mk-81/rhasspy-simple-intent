class BaseIntentHandler():
	def __init__(self, services):
		self.services = services
	
	async def initialize(self):
		pass

	async def finalize(self):
		pass