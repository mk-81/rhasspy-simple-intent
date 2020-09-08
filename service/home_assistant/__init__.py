import asyncio

from .base import *
from .light_service import LightService
from .sensor_service import SensorService
from .mediaplayer_service import MediaplayerService
from .scene_service import SceneService

class _ServiceProxy(): 
	def __init__(self,global_configuration):
		self._config = Config(global_configuration=global_configuration)
		self._config.load()
		self._endpoint_service = EndpointService(self._config)
		self.setup_services()

	def get_service_by_domain(self, domain): 
		if domain != None:
			return getattr(self, domain, None)
		else:
			return None

	def get_domain_from_entity_id(self, entity_id):
		parts = entity_id.split(".",1)
		if len(parts) == 2:
			return parts[0]
		else:
			return None

	def setup_services(self):
		self.light        = LightService(self._endpoint_service)
		self.sensor       = SensorService(self._endpoint_service)
		self.media_player = MediaplayerService(self._endpoint_service)
		self.scene        = SceneService(self._endpoint_service)

	async def finalize(self):
		await self._endpoint_service.finalize()
		

class Home_Assistant_Service():
	def __init__(self, global_configuration):
		self._global_configuration = global_configuration
		self._instance = _ServiceProxy(global_configuration=global_configuration)

	def get_instance(self):
		return self._instance

	async def finalize(self):
		await self._instance.finalize()
