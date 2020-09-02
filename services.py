class Services():
	def __init__(self, **kwargs):
		self._service_names = []
		for key in kwargs:
			self._service_names.append(key)
			setattr(self, key, kwargs[key])

	async def finalize(self):
		for sn in self._service_names:
			service = getattr(self, sn, None)
			if service != None:
				fn = getattr(service, "finalize", None)
				if callable(fn):
					await service.finalize()