from .base import AbstractService

class SensorService(AbstractService):
	def _init_int(self):
		self._service_name = "sensor"
		self._default_entity_name = "sensor"

